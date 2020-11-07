from enum import IntEnum

# Enumerator to define the different type of command messages
from SocketServer.MessageWrappers.BaseMessageData import BaseMessageData


class CmdTypes(IntEnum):
    # Command for starting and stopping the stream
    STREAM_COMMAND = 0
    TEST_COMMAND = -1


class CommandMessage(BaseMessageData):
    def __init__(self, command_type):
        super().__init__()
        self.command_type = command_type

        # This level of inheritance adds 4 bytes
        self.size += 4


# Command for starting and stopping the stream
class StreamCommand(CommandMessage):
    START_STREAM = 1
    END_STREAM = 2

    def __init__(self, mode):
        super().__init__(CmdTypes.STREAM_COMMAND)
        self.mode = mode
        # This step also ends up only adding 4 bytes
        self.size += 4


# Test command for testing things
class TestCommand(CommandMessage):
    def __init__(self):
        super().__init__(CmdTypes.TEST_COMMAND)
