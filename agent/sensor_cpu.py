import sys
import ure
from utils import cmd

class CpuSensor:

    def __init__(self, id="", freq=0):
        platform = sys.platform
        if platform == 'linux':
            self.command = 'top -b -n2 -p 1 | fgrep "Cpu(s)" | tail -1 | awk -F\'id,\' -v prefix="$prefix" \'{ split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf "%s%.1f", prefix, 100 - v }\''
            self.frequency = self.frequency_linux
            self.cores = self.cores_linux
        elif platform == 'darwin':
            # Assuming macOS
            self.frequency = self.frequency_darwin
            self.cores = self.cores_darwin
            self.command = "ps -A -o %cpu | awk '{s+=$1} END {print s}'"
        else:
            raise NotImplementedError("Platform not supported: {0}".format(platform))
        self.sensor_id = 'cpu'
        self.info = dict(
            uom = '%',
            type = 'cpu',
            freq = freq,
            label = 'CPU Usage',
            frequency = self.frequency(),
            cores = self.cores(),
            id = id)
    
    def frequency_linux(self):
        frequency = int(ure.search("CPU MHz:\s+([0-9.]+)", cmd('lscpu | grep "CPU MHz:"')).group(1))
        return "{0}MHz".format(frequency)

    def cores_linux(self):
        return ure.search("CPU(s):\s+(\d+)", cmd('lscpu | grep CPU\(s\):')).group(1)
    

    def frequency_darwin(self):
        frequency = int(int(ure.search("hw.cpufrequency:\s+(\d+)", cmd('sysctl hw.cpufrequency')).group(1))/1000000)
        return "{0}MHz".format(frequency)

    def cores_darwin(self):
        return ure.search("hw.physicalcpu:\s+(\d+)", cmd('sysctl hw.physicalcpu')).group(1)
    
    def sample(self):
        return float(cmd(self.command))
