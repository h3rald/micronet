import sys
if sys.implementation.name == 'cpython':
    from os import uname
    import json
    import asyncio
    from thingflow.base import Scheduler, SensorAsOutputThing
else:
    import ujson as json
    from thingflow import *
    from os import uname, dupterm
    import machine

from utils import *
from mqtt_connector import MQTTConnector
from config import Config

class StdoutConnector:
    def __init__(self, info):
        self.info = info
        self.logger = Logger()

    def on_next(self, x):
        self.logger.info("{0} ({1}): {2}{3}".format(self.info['label'], self.info['id'], x[2], self.info['uom']))

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
        uart = machine.UART(0, 115200)
        dupterm(uart)

        if machine.reset_cause() != machine.SOFT_RESET:
            from network import WLAN
            wl = WLAN()
            wl.mode(WLAN.STA)
            original_ssid = wl.ssid()
            original_auth = wl.auth()
            self.logger.notice("Scanning for known wifi networks...")
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
                self.logger.warning("Failed to connect to any known network, going into AP mode")
                wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
                raise
    
    def getOsData(self):
        u = uname()
        res = dict()
        res['architecture'] = u.machine
        res['kernel'] = u.sysname
        res['version'] = u.release
        return res

    def start(self):
        self.conn.connect()
        self.conn.publish('micronet/devices/' + self.id + '/online', 'true', retain=True, qos=1)
        self.conn.publish('micronet/devices/' + self.id + '/info', json.dumps(self.data), retain=True, qos=1)
        self.scheduler.run_forever()

    def schedule(self):
        self.logger.info("Scheduling sensors...")
        for k, v in self.sensors.items():
            id = k.split(':')[0]
            module = __import__("sensor_" + id)
            SensorClass = getattr(module, to_pascal_case(id + "_sensor"))
            v['id'] = k
            sensor = SensorClass(**v)
            sensor_output = SensorAsOutputThing(sensor)
            self.data['sensors'][k] = sensor.info
            sensor_output.connect(StdoutConnector(sensor.info))
            sensor_output.connect(self.conn.writer(k))
            self.scheduler.schedule_periodic(sensor_output, v['freq'])
            self.logger.info("Sensor '{0}' sampling every {1}s".format(k, v['freq']))
