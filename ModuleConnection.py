# This defines a class that encapsulates the information needed to facilitate a connection in the IPC manager

class ModuleConnection:
    def __init__(self, pipe, module_name):
        self.pipe = pipe
        self.module_name = module_name

