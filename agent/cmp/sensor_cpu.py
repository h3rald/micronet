import psutil
from cpuinfo import get_cpu_info 

class CpuSensor:

    def __init__(self, id="", freq=5):
        self.sensor_id = 'cpu'
        self.info = dict(
            uom = '%',
            type = 'cpu',
            freq = freq,
            label = 'CPU Usage',
            frequency = get_cpu_info()['hz_advertised'],
            cores = psutil.cpu_count(),
            id = id)
    
    def sample(self):
        return psutil.cpu_percent(1)
