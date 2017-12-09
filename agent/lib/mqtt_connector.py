# Based on: https://github.com/mpi-sws-rse/thingflow-python/blob/master/micropython/mqtt_writer.py

import sys
from utils import *
from config import Config

if sys.implementation.name == 'cpython':
    import paho.mqtt.client as mqtt
    import json
    import ssl
else:
    from utime import sleep_ms
    from umqtt.robust import MQTTClient as mqtt
    import ujson as json

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
    class MQTTConnector:

        def __init__(self, id):
            self.id = id;
            self.logger = Logger()
            self.config = Config()
            self.client = mqtt(
                self.config.get('id'),
                self.config.get('server'),
                port=self.config.get('port'),
                ssl=True,
                user=self.config.get('username'),
                password=self.config.get('password')
            )

        def writer(self, sensor, info):
            return MQTTConnectorWriter(self, self.id, sensor, info)

        def connect(self):
            self.logger.info("MQTT - Connecting to server...")
            self.client.connect()
            self.logger.notice("MQTT - Connection successful.")

        def set_last_will(self, topic, value):
            self.client.set_last_will(topic, value, retain=True, qos=0)

        def publish(self, topic, message, retain=True, qos=0):
            self.logger.info("MQTT - Publishing to:", topic)
            try:
                self.client.publish(topic, message, retain=retain, qos=qos)
                self.logger.info("MQTT - Message Published.")
            except Exception as ex:
                self.logger.warning("MQTT - Error:", ex)


