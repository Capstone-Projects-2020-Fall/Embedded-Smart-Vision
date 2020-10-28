# This is the data structure used to ensure messages are consistant throughout the program
class ModuleMessage:
    def __init__(self, target, tag, message):
        self.target = target
        self.tag = tag
        self.message = message
