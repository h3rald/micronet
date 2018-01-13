from bluepy import btle
import time

data = None
scanning = False
scanner = btle.Scanner().withDelegate(btle.DefaultDelegate())
temperature = 0 
battery = 0
light = 0

def scan(name, freq):
    global scanning
    global data
    global battery
    global temperature
    global light
    puck = None
    scanning = True
    devices = scanner.scan(freq)
    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if desc == 'Complete Local Name' and value == name:
                puck = dev
    if puck:
        for (adtype, desc, value) in puck.getScanData():
            if desc == 'Manufacturer':
                data = [int(x) for x in bytearray.fromhex(value)]
    scanning = False
    battery = data[7]
    temperature = data[8]
    light = data[9]


class LightSensor:

    def __init__(self, id="", unit="puckjs", name="pck:H3", freq=10):
        self.sensor_id = id
        self.name = name
        self.freq = freq
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Light',
            uom='%',
            freq = freq
        )

    def sample(self):
        global light
        global scanning
        global scan
        if not scanning:
            scan(self.name, self.freq/2)
        return light

class TemperatureSensor:

    def __init__(self, id="", unit="puckjs", name="pck:H3", freq=10):
        self.sensor_id = id
        self.name = name
        self.freq = freq
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Temperature',
            uom='°C',
            freq = freq
        )

    def sample(self):
        global temperature
        global scanning
        global scan
        if not scanning:
            scan(self.name, self.freq/2)
        return temperature

class BatterySensor:

    def __init__(self, id="", unit="puckjs", name="pck:H3", freq=10):
        self.sensor_id = id
        self.name = name
        self.freq = freq
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Battery',
            uom='%',
            freq = freq
        )

    def sample(self):
        global battery
        global scanning
        global scan
        if not scanning:
            scan(self.name, self.freq/2)
        return battery 
