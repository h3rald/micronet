from utils import cpython_sensor
import psutil

class CpuSensor:

    def __init__(self, id="", freq=0):
        cpython_sensor()
        self.sensor_id = 'cpu'
        self.info = dict(
            uom = '%',
            type = 'cpu',
            freq = freq,
            label = 'CPU Usage',
            frequency = psutil.cpu_freq().max,
            cores = psutil.cpu_count(),
            id = id)
    
    def sample(self):
        return psutil.cpu_percent(1)
