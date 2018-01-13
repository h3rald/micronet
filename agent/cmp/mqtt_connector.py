# Based on: https://github.com/mpi-sws-rse/thingflow-python/blob/master/micropython/mqtt_writer.py

import sys
import paho.mqtt.client as mqtt
import json
import ssl
from utils import *

class MQTTConnectorWriter:

    def __init__(self, connector, id, sensor, info, topic=None):
        self.id = id
        self.logger = Logger()
        self.connector = connector
        self.info = info
        self.topic = topic or "micronet/devices/{0}/data/{1}".format(id, sensor)

    def on_next(self, msg):
        self.connector.publish(self.topic, json.dumps(msg[2]))

    def on_completed(self):
        self.logger.notice("MQTT - Completed.")

    def on_error(self, e):
        self.logger.error("MQTT - Error: %s." %e)
    

class MQTTConnector:

    def __init__(self, id):
        self.id = id;
        self.logger = Logger()
        self.config = Config()
        self.client = mqtt.Client(client_id=self.id)

    def writer(self, sensor, info, topic=None):
        return MQTTConnectorWriter(self, self.id, sensor, info, topic=topic)

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
