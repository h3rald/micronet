from utils import upython_sensor
upython_sensor()
from bme280 import BME280
from machine import I2C

bme280 = None

class Bme280Sensor:

    def __init__(self, id="", unit="bme280", sda="P9", scl="P10", freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='BME280',
            freq = freq,
            data = dict(
                temperature=dict(
                    uom='°C',
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
        global bme280
        if (bme280):
            self.bme280 = bme280
        else:
            self.i2c = I2C(0, I2C.MASTER, pins=(sda, scl))
            self.bme280 = BME280(i2c=self.i2c)
            bme280 = self.bme280
    
    def sample(self):
        data = self.bme280.read_compensated_data()
        return dict(temperature=data[0]/100, pressure=data[1]/25600, humidity=data[2]/1000)

class Bme280TemperatureSensor:

    def __init__(self, id="", unit="bme280", sda="P9", scl="P10", freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Temperature',
            uom='°C',
            freq = freq
        )
        global bme280
        if (bme280):
            self.bme280 = bme280
        else:
            self.i2c = I2C(0, I2C.MASTER, pins=(sda, scl))
            self.bme280 = BME280(i2c=self.i2c)
            bme280 = self.bme280
    
    def sample(self):
        return self.bme280.read_compensated_data()[0]/100

class Bme280PressureSensor:

    def __init__(self, id="", unit="bme280", sda="P9", scl="P10", freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Pressure',
            uom='hPa',
            freq = freq
        )
        global bme280
        if (bme280):
            self.bme280 = bme280
        else:
            self.i2c = I2C(0, I2C.MASTER, pins=(sda, scl))
            self.bme280 = BME280(i2c=self.i2c)
            bme280 = self.bme280
    
    def sample(self):
        return self.bme280.read_compensated_data()[1]/25600

class Bme280HumiditySensor:

    def __init__(self, id="", unit="bme280", sda="P9", scl="P10", freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type = unit,
            label='Pressure',
            uom='%',
            freq = freq
        )
        global bme280
        if (bme280):
            self.bme280 = bme280
        else:
            self.i2c = I2C(0, I2C.MASTER, pins=(sda, scl))
            self.bme280 = BME280(i2c=self.i2c)
            bme280 = self.bme280
    
    def sample(self):
        return self.bme280.read_compensated_data()[2]/1000

