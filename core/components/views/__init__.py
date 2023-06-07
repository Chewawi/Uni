import importlib

class Views:
    ...

module = importlib.import_module('.buttons', __package__)
for name in dir(module):
    if not name.startswith('__'):
        setattr(Views, name, getattr(module, name))