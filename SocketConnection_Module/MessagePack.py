# Holds flags used to define message types inside of a packet
from enum import Enum
from socket import socket


class MsgType(Enum):
    INVALID = -1
    SINGLE_IMAGE = 1
    TEXT_MESSAGE = 2
    COMMAND = 3


# Abstraction meant to separate and encapsulate the data needed for the header
class Header:
    HEADER_SIZE = 8

    def __init__(self,
                 message_type=MsgType.INVALID,
                 data_length=0):
        # The length of the data in the packet
        self.data_length = data_length
        self.messageType = message_type

    # Create the byte array for the header
    def encode_header(self):
        pass


# Unified system for holding messages, gives a standard interface
# through which we can serialize and deserialize data
class MessagePack:
    HEADER_SIZE = 0

    def __init__(self,
                 message_type=MsgType.INVALID,
                 data_length=0):
        self.header = Header(message_type=message_type, data_length=data_length)

        # This is the raw bytes for the message
        self.raw_data = None

    def print_package(self):
        print("Length: ", self.header.data_length, "\n",
              "Message Type: ", self.header.messageType)


# Helper class to read and reconstruct bytes that may have been coalesced by the socket
def get_bytes(cnt: int, conn: socket):
    buf_size = 4096
    remaining_bytes = cnt
    data = bytearray()
    while True:
        if remaining_bytes < buf_size:
            # If we have less bytes remaining
            # to receive then the buffer size receive only those bytes
            tmp = conn.recv(remaining_bytes)
            data.extend(tmp)
            break
        else:
            # If we are still taking full buffers take full buffers
            data += conn.recv(buf_size)
            # Keep track of how many bytes we have consumed
            remaining_bytes = remaining_bytes - buf_size

    return data
