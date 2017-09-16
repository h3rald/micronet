import sys
from utils import cmd

class CpuSensor:

    def __init__(self):
        platform = sys.platform
        if platform == 'linux':
            self.command = 'top -b -n2 -p 1 | fgrep "Cpu(s)" | tail -1 | awk -F\'id,\' -v prefix="$prefix" \'{ split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf "%s%.1f", prefix, 100 - v }\''
        elif platform == 'darwin':
            # Assuming macOS
            self.command = "ps -A -o %cpu | awk '{s+=$1} END {print s}'"
        else:
            raise NotImplementedError("Platform not supported: {0}".format(platform))
        self.sensor_id = 'cpu'
        self.info = dict(
            uom = '%',
            label = 'CPU Usage',
            id = 'cpu')
    
    def sample(self):
        return float(cmd(self.command))
