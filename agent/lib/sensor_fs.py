from utils import cpython_sensor
cpython_sensor()
import psutil

class FsSensor:

    def __init__(self, id="", mount="", device="", freq=0):
        self.sensor_id = id
        self.info = dict(
            uom = '%',
            type =  "fs",
            label = 'Disk Usage',
            device = device,
            mount = mount,
            freq = freq,
            id = self.sensor_id,
            total = "{0}GB".format(int(psutil.disk_usage(mount).total/(1024*1024*1024)))
        )
    
    def sample(self):
        return psutil.disk_usage(self.info['mount']).percent
