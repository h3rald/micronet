from utils import upython_sensor
upython_sensor()
from ds18x20 import DS18X20
from onewire import OneWire
from time import sleep_ms
from machine import Pin


class TemperatureSensor:

    def __init__(self, id="", unit="ds18b20", pin=4, freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Temperature',
            uom='°C',
            freq = freq
        )
        self.ds = DS18X20(OneWire(Pin(pin)))
        self.rom = self.ds.scan()[0]

    def sample(self):
        self.ds.convert_temp()
        sleep_ms(750)
        return self.ds.read_temp(self.rom)
