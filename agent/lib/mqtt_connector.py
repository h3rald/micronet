# Based on: https://github.com/mpi-sws-rse/thingflow-python/blob/master/micropython/mqtt_writer.py

import sys

if sys.implementation.name == 'cpython':
    import paho.mqtt.client as mqtt
    import json
    import ssl
else:
    import gc
    import umqtt.simple 
    import utime
    import ujson as json

from utils import *
from config import Config

class MQTTConnectorWriter:

    def __init__(self, connector, id, sensor, info):
        self.id = id
        self.logger = Logger()
        self.connector = connector
        self.info = info
        self.topic = "micronet/devices/{0}/data/{1}".format(id, sensor)

    def on_next(self, msg):
        self.connector.publish(self.topic, json.dumps(msg[2]))

    def on_completed(self):
        self.logger.notice("MQTT - Completed.")

    def on_error(self, e):
        self.logger.error("MQTT - Error: %s." %e)
    

if sys.implementation.name == 'cpython':

    class MQTTConnector:

        def __init__(self, id):
            self.id = id;
            self.logger = Logger()
            self.config = Config()
            self.client = mqtt.Client(client_id=self.id)

        def writer(self, sensor, info):
            return MQTTConnectorWriter(self, self.id, sensor, info)

        def connect(self):
            if self.config.get("ssl"):
                ssl_ctx = ssl.create_default_context()
                ssl_ctx.check_hostname = False
                self.client.tls_set_context(ssl_ctx)
                # Do not enforce TLS verification
                self.client.tls_insecure_set(True) 
            self.client.username_pw_set(self.config.get('username'), self.config.get('password'))
            self.logger.info("MQTT - Connecting to server...")
            self.client.connect(self.config.get('server'), self.config.get('port'))
            self.logger.notice("MQTT - Connection successful.")
            self.client.loop_start()

        def set_last_will(self, topic, value):
            self.client.will_set(topic, payload=value, retain=True, qos=1)

        def publish(self, topic, message, retain=True, qos=1):
            self.logger.info("MQTT - Publishing to:", topic)
            out = self.client.publish(topic, payload=message, retain=retain, qos=qos)
            if out[0] == mqtt.MQTT_ERR_SUCCESS:
                self.logger.info("MQTT - Message Published.")
            else:
                self.logger.warning("MQTT - Error:", mqtt.error_string(out[0]))

else:

    class MQTTClient(umqtt.simple.MQTTClient):

        def __init__(self, client_id, server, port=0, user=None, password=None, ssl=False):
            super().__init__(client_id, server, port=port, user=user, password=password, keepalive=0, ssl=ssl)
            self.logger = Logger()

        def delay(self, i):
            utime.sleep(i)

        def connect(self, clean_session=True):
            super().connect(clean_session=clean_session)

        def reconnect(self):
            super().close()
            i = 0
            while 1:
                try:
                    return super().connect(True)
                except OSError as e:
                    self.logger.warning(e)
                    i += 1
                    self.delay(i)

        def reset(self):
            self.logger.warning('Connection error detected. Resetting board in 20s...')
            delayed_reset()

        def publish(self, topic, msg, retain=False, qos=0):
            while 1:
                try:
                    return super().publish(topic, msg, retain, qos)
                except OSError as e:
                    self.logger.warning(e)
                self.reset()
                #self.reconnect()

        def wait_msg(self):
            while 1:
                try:
                    return super().wait_msg()
                except OSError as e:
                    self.logger.warning(e)
                self.reset()
                #self.reconnect()


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

        def writer(self, sensor, info):
            return MQTTConnectorWriter(self, self.id, sensor, info)

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

