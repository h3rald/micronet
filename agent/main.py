import sys
sys.path.append('lib')
sys.path.append('vendor')

from agent import Agent
from utils import delayed_reset
import gc

try:
    AGENT = Agent()
    AGENT.wifi_connect()
    gc.collect()
    AGENT.schedule_machine_reset()
    AGENT.schedule()
    gc.collect()
    AGENT.start()
except Exception as e:
    print('ERROR: An unhandled exception was raised.')
    print(e)
    print("-> Resetting board in 20s...")
    delayed_reset()
    

while True:
    pass
