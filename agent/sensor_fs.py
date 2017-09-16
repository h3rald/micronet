import ure
import sys
from utils import cmd

class FsSensor:

    def __init__(self, id="", mount="", device="", freq=0):
        self.command = 'df -P | grep {0}'.format(device)
        self.sensor_id = id
        self.info = dict(
            uom = '%',
            type =  "fs",
            label = 'Disk Usage',
            device = device,
            mount = mount,
            freq = freq,
            id = self.sensor_id)
        total_regex = "[^\s]\s+([0-9a-zA-Z.]+)"
        total_cmd = 'df -H | grep {0}'.format(device)
        self.info['total'] = ure.search(total_regex, cmd(total_cmd)).group(1) + 'B'
    
    def sample(self):
        raw = cmd(self.command)
        regex = "[^\s]+\s+\d+\s+\d+\s+\d+\s+(\d+)%"
        m = ure.search(regex, raw)
        return int(m.group(1))
