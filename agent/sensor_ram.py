import ure
import sys
from utils import cmd

class RamSensor:

    def __init__(self):
        platform = sys.platform
        if platform == 'linux':
            self.command = 'free | grep Mem'
            self.sample = self.sample_linux
        elif platform == 'darwin':
            self.command = 'top -l 1 |  grep PhysMem'
            self.sample = self.sample_darwin
        else:
            raise NotImplementedError("Platform not supported: {0}".format(platform))
        self.sensor_id = 'ram'
        self.info = dict(
            uom = '%',
            label = 'RAM Usage',
            id = 'ram')

    def sample_linux(self):
        regex = "Mem:\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)"
        m = ure.search(regex, cmd(self.command))
        avail = int(m.group(2))
        total = int(m.group(1))
        used = total - avail
        return used*100/total

    def sample_darwin(self):
        regex = "PhysMem: (\d+)M used \((\d+)M wired\), (\d+)M unused."
        m = ure.search(regex, cmd(self.command))
        used = int(m.group(1))
        unused = int(m.group(3))
        total = used + unused
        return used*100/total
