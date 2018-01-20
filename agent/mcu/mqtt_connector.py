# Based on: https://github.com/mpi-sws-rse/thingflow-python/blob/master/micropython/mqtt_writer.py

import umqtt_simple
import sys
import utime
import ujson
from utils import *

class MQTTConnectorWriter:

    def __init__(self, connector, id, sensor, info, topic=None):
        self.id = id
        self.logger = Logger()
        self.connector = connector
        self.info = info
        self.topic = topic or "micronet/devices/{0}/data/{1}".format(id, sensor)

    def on_next(self, msg):
        self.connector.publish(self.topic, ujson.dumps(msg[2]))

    def on_completed(self):
        self.logger.notice("MQTT - Completed.")

    def on_error(self, e):
        self.logger.error("MQTT - Error: %s." %e)
    

class MQTTClient(umqtt_simple.MQTTClient):

    def __init__(self, client_id, server, port=0, user=None, password=None, ssl=False):
        super().__init__(client_id, server, port=port, user=user, password=password, keepalive=0, ssl=ssl)
        self.logger = Logger()

    def delay(self, i):
        utime.sleep(i)

    def connect(self, clean_session=True):
        super().connect(clean_session=clean_session)

    def reset(self):
        self.logger.warning('Connection error.')
        delayed_reset()

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.logger.warning(e)
            self.reset()

    def wait_msg(self):
        while 1:
            try:
                return super().wait_msg()
            except OSError as e:
                self.logger.warning(e)
            self.reset()


class MQTTConnector:

    def __init__(self, id):
        self.id = id;
        self.logger = Logger()
        self.config = Config()
        self.client = MQTTClient(
            self.config.get('id'),
            self.config.get('server'),
            port=self.config.get('port'),
            user=self.config.get('username'),
            password=self.config.get('password')
        )

    def set_last_will(self, topic, value):
        self.client.set_last_will(topic, value)

    def publish(self, topic, msg, retain=False, qos=0):
        self.client.publish(bytes(topic, 'utf-8'), bytes(msg, 'utf-8'), retain, qos)

    def writer(self, sensor, info, topic=None):
        return MQTTConnectorWriter(self, self.id, sensor, info, topic=topic)

    def connect(self):
        self.logger.info("MQTT - Connecting to server...")
        try:
            self.client.connect()
        except OSError as e:
            self.logger.warning('Connection Error:', e)
            self.client.reset()
        self.logger.notice("MQTT - Connection successful.")

        def set_last_will(self, topic, value):
            self.client.set_last_will(topic, value, retain=True, qos=0)

        def publish(self, topic, message, retain=True, qos=0):
            self.logger.info("MQTT - Publishing to:", topic)
            self.client.publish(bytes(topic, 'utf-8'), bytes(message, 'utf-8'), retain=retain, qos=qos)
            self.logger.info("MQTT - Message Published.")

