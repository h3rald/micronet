from utils import cpython_sensor
cpython_sensor()
import psutil

class RamSensor:

    def __init__(self, id="", freq=0):
        self.sensor_id = 'ram'
        self.info = dict(
            uom = '%',
            type = 'ram',
            freq = freq,
            label = 'RAM Usage',
            total = "{0}MB".format(int(psutil.virtual_memory().total/(1024*1024))),
            id = id)

    def sample(self):
        mem = psutil.virtual_memory()
        return float('%.2f'%((mem.total - mem.available)*100/mem.total))
