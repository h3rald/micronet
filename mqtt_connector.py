# Based on: https://github.com/mpi-sws-rse/thingflow-python/blob/master/micropython/mqtt_writer.py

import sys
from utils import *
from config import Config
import ujson
sys.path.append('vendor')
from umqtt.robust import MQTTClient

class MQTTConnector:

    def __init__(self, id, topic=None, connect=True):
        self.logger = Logger()
        self.id = id
        self.config = Config()
        self.topic = topic
        self.client = MQTTClient(
            client_id=self.id,
            server=self.config.get('server'),
            port=self.config.get('port'),
            ssl=True,
            user=self.config.get('username'),
            password=self.config.get('password')
        )
        if connect:
            self.connect()

    def connect(self):
        self.logger.info(self.label(), "Connecting to MQTT Broker...")
        self.client.connect()
        self.logger.notice(self.label(), "Connection successful.")

    def label(self):
        return "{%s}" % self.id

    def set_last_will(self, topic, value):
        self.client.set_last_will(topic, value, retain=True, qos=1)

    def publish(self, topic, message, retain=False, qos=0):
        self.logger.info(self.label(), "Publishing to:", topic)
        self.client.publish(bytes(topic, 'utf-8'), bytes(message, 'utf-8'), retain, qos)

    def on_next(self, msg):
        self.logger.info(self.label(), "Publishing to:", self.topic)
        data = bytes(ujson.dumps(msg), 'utf-8')
        self.client.publish(bytes(self.topic, 'utf-8'), data)

    def on_completed(self):
        self.logger.notice(self.label(), "Completed - Disconnecting.")
        self.client.disconnect()

    def on_error(self, e):
        self.logger.error(self.label(), "Error: %s - Disconnecting." %e)
        self.client.disconnect()
