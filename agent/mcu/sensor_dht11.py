from machine import Pin
from dht import DHT11

dht = None

class HumiditySensor:

    def __init__(self, id="", unit="dht11", pin=2, freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Humidity',
            uom='%',
            freq = freq
        )
        global dht
        if (not dht):
            dht = DHT11(Pin(pin))

    def sample(self):
        dht.measure()
        return dht.humidity()

class TemperatureSensor:

    def __init__(self, id="", unit="dht11", pin=2, freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Temperature',
            uom='°C',
            freq = freq
        )
        global dht
        if (not dht):
            dht = DHT11(Pin(pin))

    def sample(self):
        dht.measure()
        return dht.temperature()
