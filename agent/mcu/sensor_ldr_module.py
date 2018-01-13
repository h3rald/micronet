from machine import Pin

class LightSensor:

    def __init__(self, id="", unit="LDR Module", pin=5, freq=5):
        self.sensor_id = id
        self.info = dict(
            id = self.sensor_id,
            type =  unit,
            label='Light',
            uom='',
            freq = freq
        )
        self.ldr = Pin(pin)

    def sample(self):
        if self.ldr.value() == 0:
            return 'on'
        else:
            return 'off'
