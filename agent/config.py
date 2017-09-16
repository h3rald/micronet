import ujson
import uio
from utils import Singleton

class Config(Singleton):

    __getattr__= dict.__getitem__

    def __init__(self):
        f = uio.open('config.json')
        self._data = ujson.loads(f.read())
        f.close()

    def get(self, s):
        path = s.split('.')
        data = self._data
        for segment in path:
            if segment in data:
                data = data[segment]
            else:
                return None
        return data
