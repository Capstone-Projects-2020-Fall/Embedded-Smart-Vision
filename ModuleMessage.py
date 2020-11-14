# This is the data structure used to ensure messages are consistant throughout the program
class ModuleMessage:
    def __init__(self, target, tag, message, optional_tag='NOT_SET'):
        self.target = target
        self.tag = tag
        self.message = message
        self.optional_tag = optional_tag
