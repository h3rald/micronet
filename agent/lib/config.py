import utils
import sys

if sys.implementation.name == 'cpython':
    import json
    import io
else:
    import ujson as json
    import uio as io

class Config(utils.Singleton):

    __getattr__= dict.__getitem__

    def __init__(self):
        f = io.open('config.json')
        self._data = json.loads(f.read())
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
