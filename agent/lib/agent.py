import sys

from mqtt_connector import MQTTConnector
from utils import *
from config import Config

if sys.implementation.name == 'cpython':
    from os import uname
    import json
    import asyncio
    from thingflow.base import Scheduler, SensorAsOutputThing
else:
    from thingflow import *
    import ujson as json
    from os import uname, dupterm
    import machine

    class Resetter:

        def __init__(self, freq=10, max=180):
            self.freq = freq
            self.max = max
            self.value = 0
            self.logger = Logger()
            self.sensor_id = 'resetter'
    
        def sample(self):
            self.value = self.value + self.freq
            self.logger.info('-- Board reset scheduled in {}s.'.format(self.max - self.value))
            if (self.value >= self.max):
                self.logger.info('Resetting board...')
                start_reset()
            return 1

class Informer:
    def __init__(self, id="", conn=None, data=None):
        self.logger = Logger()
        self.conn = conn
        self.id = id
        self.data = data
        self.info = dict()
        self.info['label'] = 'Online Status'
        self.info['id'] = id
        self.info['uom'] = ''
        self.sensor_id = 'informer'
    
    def sample(self):
        return True

class StdoutConnector:
    def __init__(self, info):
        self.info = info
        self.logger = Logger()

    def on_next(self, x):
        value = x[2]
        if type(value) == dict:
            data = self.info['data']
            # Print multiple values, assuming labels and uoms are in info['data']
            for key, val in data.items():
                self.logger.info("{0} ({1}): {2}{3}".format(val['label'], self.info['id'], value[key], val['uom']))
        else:
            self.logger.info("{0} ({1}): {2}{3}".format(self.info['label'], self.info['id'], value, self.info['uom']))

    def on_completed():
        self.logger.info("[stdout-connector] Completed.")

    def on_error(self, e):
        self.logger.info("[stdout-connector] Error:", e)
        sys.exit()

class Agent:
    
    def __init__(self):
        self.logger = Logger()
        self.config = Config()
        self.id = self.config.get('id')
        self.type = self.config.get('type')
        self.sensors = self.config.get('sensors')
        self.data = dict()
        self.data['id'] = self.id
        self.data['type'] = self.type
        self.data['model'] = self.config.get('model')
        self.data['implementation'] = dict()
        self.data['implementation']['name'] = sys.implementation.name
        self.data['implementation']['version'] = '.'.join(str(x) for x in sys.implementation.version)
        self.data['platform'] = sys.platform
        self.data['sensors'] = dict()
        self.data['os'] = self.getOsData()
        self.logger.notice("MicroNet Agent started on %s (%s)" % (self.id, self.type))
        self.conn = MQTTConnector(self.id)
        self.conn.set_last_will('micronet/devices/' + self.id + '/online', 'false')
        if sys.implementation.name == 'cpython':
            self.scheduler = Scheduler(asyncio.get_event_loop())
        else:
            self.scheduler = Scheduler()

    def wifi_connect(self):
        self.networks = self.config.get('wifi')
        import network
        wl = network.WLAN()
        tuple_wifi_api = True
        try:
            wl.mode(network.WLAN.STA)
        except AttributeError:
            tuple_wifi_api = False
            sta = network.WLAN(network.STA_IF)
            ap = network.WLAN(network.AP_IF)
            sta.active(True)
            ap.active(False)
        self.logger.notice("Scanning for known wifi networks...")
        if tuple_wifi_api:
            available_nets = wl.scan()
            nets = frozenset([e.ssid for e in available_nets])
            known_nets_names = frozenset([key for key in self.networks])
            net_to_use = list(nets & known_nets_names)
            try:
                net_to_use = net_to_use[0]
                net_properties = self.networks[net_to_use]
                pwd = net_properties['password']
                sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
                if 'config' in net_properties:
                    wl.ifconfig(config=tuple(net_properties['config']))
                wl.connect(net_to_use, (sec, pwd), timeout=10000)
                while not wl.isconnected():
                    machine.idle() # save power while waiting
                self.logger.notice("Connected to "+net_to_use+" with IP address:" + wl.ifconfig()[0])
            except Exception as e:
                self.logger.warning(e)
                self.logger.warning("Failed to connect to any known network. Resetting board in 20s.")
                delayed_reset()
        else:
            available_nets = wl.scan()
            nets = frozenset(str(bytearray(e[0]), "utf-8") for e in available_nets)
            known_nets_names = frozenset([key for key in self.networks])
            net_to_use = list(nets & known_nets_names)
            try:
                net_to_use = net_to_use[0]
                net_properties = self.networks[net_to_use]
                pwd = net_properties['password']
                wl.connect(net_to_use, pwd)
                while not wl.isconnected():
                    machine.idle() # save power while waiting
                self.logger.notice("Connected to "+net_to_use+" with IP address:" + wl.ifconfig()[0])
            except Exception as e:
                self.logger.warning(e)
                self.logger.warning("Failed to connect to any known network. Resetting board in 20s.")
                delayed_reset()
    
    def getOsData(self):
        u = uname()
        res = dict()
        res['architecture'] = u.machine
        res['kernel'] = u.sysname
        res['version'] = u.release
        return res

    def start(self):
        self.conn.connect()
        self.conn.publish('micronet/devices/' + self.id + '/online', 'true', retain=True, qos=0)
        self.conn.publish('micronet/devices/' + self.id + '/info', json.dumps(self.data), retain=True, qos=0)
        self.scheduler.run_forever()

    def schedule_machine_reset(self):
        if (self.config.get('reset')):
            freq = self.config.get('reset.freq')
            resetter = Resetter(freq=10, max=freq)
            resetter_out = SensorAsOutputThing(resetter)
            self.scheduler.schedule_periodic(resetter_out, 10)
            self.logger.info('Scheduled automatic board reset every {0} seconds.'.format(freq))

    def schedule(self):
        self.logger.info("Scheduling sensors...")
        informer = Informer(data=self.data, id=self.id, conn=self.conn)
        informer_out = SensorAsOutputThing(informer)
        informer_out.connect(StdoutConnector(informer.info))
        informer_out.connect(self.conn.writer('informer', informer.info, topic='micronet/devices/' + self.id + '/online'))
        self.scheduler.schedule_periodic(informer_out, 5)
        for k, v in self.sensors.items():
            id = k.split(':')[0]
            unit = id
            if 'unit' in v: 
                unit = v['unit']
            try:
                module = __import__("sensor_" + unit)
                SensorClass = getattr(module, to_pascal_case(id + "_sensor"))
                v['id'] = k
                sensor = SensorClass(**v)
                sensor_output = SensorAsOutputThing(sensor)
                self.data['sensors'][k] = sensor.info
                sensor_output.connect(StdoutConnector(sensor.info))
                sensor_output.connect(self.conn.writer(k, sensor.info))
                self.scheduler.schedule_periodic(sensor_output, v['freq'])
                self.logger.info("Sensor '{0}' sampling every {1}s".format(k, v['freq']))
            except Exception as e:
                self.logger.warning(e)
                if sys.implementation.name == 'micropython':
                    self.logger.warning("Resetting board in 20s.")
                    delayed_reset()
