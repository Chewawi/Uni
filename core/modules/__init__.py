import importlib
import os

class Uni:
    ...

items = os.listdir('./core/modules')
files = [item for item in items if os.path.isfile(os.path.join('./core/modules', item))]

for filename in files:
    module = importlib.import_module(f'.{filename[:-3]}', __package__)
    for name in dir(module):
        if not name.startswith('__'):
            setattr(Uni, name, getattr(module, name))