# Based on: https://github.com/mpi-sws-rse/thingflow-python/blob/master/micropython/mqtt_writer.py

import sys
from utils import *
from config import Config
import ujson
sys.path.append('vendor')
from umqtt.robust import MQTTClient

class MQTTConnectorWriter:

    def __init__(self, client, id, sensor):
        self.logger = Logger()
        self.client = client
        self.topic = "micronet/devices/{0}/data/{1}".format(id, sensor)

    def on_next(self, msg):
        self.logger.info("MQTT - Publishing to:", self.topic)
        data = bytes(ujson.dumps(msg), 'utf-8')
        self.client.publish(bytes(self.topic, 'utf-8'), data)

    def on_completed(self):
        self.logger.notice("MQTT - Completed.")

    def on_error(self, e):
        self.logger.error("MQTT - Error: %s." %e)
    

class MQTTConnector:

    def __init__(self, id):
        self.id = id;
        self.logger = Logger()
        self.config = Config()
        self.client = MQTTClient(
            client_id=self.id,
            server=self.config.get('server'),
            port=self.config.get('port'),
            ssl=True,
            user=self.config.get('username'),
            password=self.config.get('password')
        )

    def writer(self, sensor):
        return MQTTConnectorWriter(self.client, self.id, sensor)

    def connect(self):
        self.logger.info("MQTT - Connecting to server...")
        self.client.connect()
        self.logger.notice("MQTT - Connection successful.")

    def set_last_will(self, topic, value):
        self.client.set_last_will(topic, value, retain=True, qos=1)

    def publish(self, topic, message, retain=False, qos=0):
        self.logger.info("MQTT - Publishing to:", topic)
        self.client.publish(bytes(topic, 'utf-8'), bytes(message, 'utf-8'), retain, qos)
