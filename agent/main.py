import sys
sys.path.append('lib')
sys.path.append('vendor')

from agent import Agent

AGENT = Agent()

AGENT.wifi_connect()
AGENT.schedule()
AGENT.start()

while True:
    pass
