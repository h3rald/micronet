import sys
sys.path.append('mcu')
from agent import Agent
import utils
import micropython

try:
    AGENT = Agent()
    AGENT.wifi_connect()
    AGENT.schedule_machine_reset()
    AGENT.schedule()
    AGENT.start()
except Exception as e:
    print('ERROR: An unhandled exception was raised.')
    sys.print_exception(e)
    micropython.mem_info(1)
    utils.blink(0x7f0000)
    utils.delayed_reset()

while True:
    pass
