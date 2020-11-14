# This file will encapsulate an interface that the outgoing thread
# Can understand and use to send messages to the central server
from enum import IntEnum


class NSM_TYPE(IntEnum):
    INVALID = -1
    TEST_MESSAGE = 1
    SEND_VIDEO = 2


class NetworkSendMessage:
    def __init__(self,
                 message_type=NSM_TYPE.INVALID,
                 var1=None,
                 var2=None,
                 var3=None,
                 var4=None):
        # Define what type of message we are sending
        self.message_type = message_type
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        self.var4 = var4
