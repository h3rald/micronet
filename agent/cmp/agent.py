import sys
from mqtt_connector import MQTTConnector
from utils import *
from os import uname
import json
import asyncio
from thingflow.base import Scheduler, SensorAsOutputThing

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
        self.scheduler = Scheduler(asyncio.get_event_loop())

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
