import sys
sys.path.append('lib')

from agent import Agent

AGENT = Agent()  

AGENT.schedule()
AGENT.start()

while True:
    pass
