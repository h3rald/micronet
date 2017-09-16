import sys
import ujson
sys.path.append('vendor')
from utils import *
from thingflow import *

from mqtt_connector import MQTTConnector
from config import Config

class StdoutConnector:
    def __init__(self, info):
        self.info = info
        self.logger = Logger()

    def on_next(self, x):
        self.logger.info("{0}: {1}{2}".format(self.info['label'], x[2], self.info['uom']))

    def on_completed():
        self.logger.info("[stdout-connector] Completed.")

    def on_error(self, e):
        self.logger.info("[stdout-connector] Error:", e)

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
        if self.type == 'computer':
            self.data['os'] = self.getOsData()
        self.logger.notice("MicroNet Agent started on %s (%s)" % (self.id, self.type))
        self.conn = MQTTConnector(self.id)
        self.conn.set_last_will('micronet/devices/' + self.id + '/online', 'true')
        self.scheduler = Scheduler()

    def getOsData(self):
        res = dict()
        res['architecture'] = cmd('uname -m')
        res['kernel'] = cmd('uname -s')
        res['version'] = cmd('uname -r')
        return res

    def start(self):
        self.conn.connect()
        self.conn.publish('micronet/devices/' + self.id + '/online', 'false', retain=True, qos=1)
        self.conn.publish('micronet/devices/' + self.id + '/info', ujson.dumps(self.data), retain=True, qos=1)
        self.scheduler.run_forever()

    def schedule(self):
        self.logger.info("Scheduling sensors...")
        for k, v in self.sensors.items():
            module = __import__("sensor_" + k)
            SensorClass = getattr(module, to_pascal_case(k + "_sensor"))
            sensor = SensorClass()
            sensor_output = SensorAsOutputThing(sensor)
            self.data['sensors'][k] = sensor.info
            sensor_output.connect(StdoutConnector(sensor.info))
            sensor_output.connect(self.conn.writer(k))
            self.scheduler.schedule_periodic(sensor_output, v['freq'])
            self.logger.info("Sensor '{0}' sampling every {1}s".format(k, v['freq']))
