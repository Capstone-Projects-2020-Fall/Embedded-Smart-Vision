# This class handles all the incoming traffic and messages
import struct
import threading
from queue import Queue
from socket import socket
from .MessagePack import MessagePack, MsgType, get_bytes, Header, build_from_bytes
from .QueueMessage import QueueMessage


class IncomingThread(threading.Thread):

    def __init__(self,
                 name: str,
                 inc_queue: Queue,
                 connection: socket):
        """
        :param name:        The name of the thread
        :param inc_queue:   This queue will hold all of the incoming information, we should only be pushing to this
        :param connection:  The socket we are listening on
        """
        # Call the supers init function
        threading.Thread.__init__(self)
        self.name: str = name
        self.running: bool = False
        self.inc_queue: Queue = inc_queue
        self.connection: socket = connection

    def run(self):
        print("Starting: " + self.name)
        self.running = True
        while self.running:
            self.running = False
            # Create a variable to hold the message we unpack
            msg_pck = None

            # Receive the header bytes
            received_bytes = get_bytes(Header.HEADER_SIZE, self.connection)

            # Check to make sure we haven't received 0 bytes which would indicate the
            # other side has closed down it's socket
            if len(received_bytes) == 4:
                print('Received improper amount of bytes count: ', len(received_bytes))
                self.running = False
                continue
            elif len(received_bytes) < 8:
                print('Received in incorrect amount of bytes, this may become an issue but not now')
                continue

            # Receive and decrypt 4 bytes to determine the message type
            data_length, msg_type = struct.unpack('ii', received_bytes)
            # collect our raw data
            raw_data = get_bytes(data_length, self.connection)

            # Create the proper message pack
            msg_pck = build_from_bytes(MsgType(msg_type), data_length, raw_data)

            # Build a queue message to track the origins of the message
            queue_message = QueueMessage(node_origin=self.name,
                                         msg_package=msg_pck)
            self.inc_queue.put(queue_message)

        self.break_down()

    def set_running(self, option: bool):
        self.running = option

    def break_down(self):
        print("Breaking down thread: " + self.name)
