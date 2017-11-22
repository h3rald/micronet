import sys
sys.path.append(‘vendor’)
try:
    import os
    def cmd(s):
        p = os.popen(s)
        lines = p.readlines()
        out = ‘’.join(map(lambda x: x.strip(), lines))
        p.close()
        return out
except ImportError:
    def cmd(s):
        return ‘’

import sys
import ure

def to_pascal_case(snake_case_str):
    parts = snake_case_str.split(‘_’)
    return “”.join(x[0].upper()+x[1:].lower() for x in parts)

class Singleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class Logger(Singleton):
    
    LEVEL = 3

    for arg in sys.argv:
        match = ure.search(“—log:(\d)”, arg)
        if match:
            LEVEL = int(match.group(1))
            break;

    def error(self, *args):
        pass

    def warning(self, *args):
        pass

    def notice(self, *args):
        pass

    def info(self, *args):
        pass

    def debug(self, *args):
        pass

    def verbose(self, *args):
        pass

    if LEVEL > 0:
        def error(self, *args):
            print(“ ERROR:”, *args)
    
    if LEVEL > 1:
        def warning(self, *args):
            print(“  WARN:”*args)
    
    if LEVEL > 2:
        def notice(self, *args):
            print(“NOTICE:”, *args)
    
    if LEVEL > 3:
        def info(self, *args):
            print(“  INFO:”, *args)
    
    if LEVEL > 4:
        def debug(self, *args):
            print(“ DEBUG:”, *args)
    
    if LEVEL > 5:
        def silly(self, *args):
            print(“ SILLY:”, *args)
