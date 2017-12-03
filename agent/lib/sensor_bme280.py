from utils import upython_sensor
upython_sensor()
from bme280 import BME280
from machine import I2C

class Bme280Sensor:

    def __init__(self, id="", sda="P9", scl="P10", freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            uom='multiple',
            type =  "bme280",
            label='BME280',
            freq = freq,
            data = dict(
                temperature=dict(
                    uom='C',
                    label='Temperature'
                ),    
                pressure=dict(
                    uom='hPa',
                    label='Pressure'
                ),    
                humidity=dict(
                    uom='%',
                    label='Humidity'
                )
            )
        )
        self.i2c = I2C(0, I2C.MASTER, pins=(sda, scl))
        self.bme280 = BME280(i2c=self.i2c)
    
    def sample(self):
        return self.bme280.values
