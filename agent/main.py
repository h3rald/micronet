import sys
sys.path.append('mcu')
from agent import Agent
from utils import delayed_reset

try:
    AGENT = Agent()
    AGENT.wifi_connect()
    AGENT.schedule_machine_reset()
    AGENT.schedule()
    AGENT.start()
except Exception as e:
    print('ERROR: An unhandled exception was raised.')
    sys.print_exception(e)
    delayed_reset()

while True:
    pass
