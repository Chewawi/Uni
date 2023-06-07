import os
import importlib

class Components:
    ...

items = os.listdir('./core/components')
files = [item for item in items if os.path.isfile(os.path.join('./core/components', item))]

for filename in files:
    module = importlib.import_module(f'.{filename[:-3]}', __package__)
    for name in dir(module):
        if not name.startswith('__'):
            setattr(Components, name, getattr(module, name))