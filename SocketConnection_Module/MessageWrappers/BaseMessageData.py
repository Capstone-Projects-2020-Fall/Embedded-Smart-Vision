# This is a class that provides the basis for all messages with important interface functions
class BaseMessageData:
    def __init__(self):
        self.size = 0

    def get_size(self):
        return self.size
