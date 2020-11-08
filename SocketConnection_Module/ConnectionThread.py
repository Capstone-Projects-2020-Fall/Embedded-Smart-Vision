# This class handles all the incoming traffic and messages
import struct
import threading
from queue import Queue
import socket
from .MessagePack import MessagePack, MsgType, get_bytes, Header

from SocketConnection_Module.IncomingThread import IncomingThread
from .OutgoingThread import OutgoingThread


class ConnectionThread(threading.Thread):

    def __init__(self, node_name='UnamedNode', context=None):
        """
        :param name:        The name of the thread
        :param inc_queue:   This queue will hold all of the incoming information, we should only be pushing to this
        :param connection:  The socket we are listening on
        """
        # Call the supers init function
        threading.Thread.__init__(self)
        self.running = False
        self.central_server_name = None
        self.node_node = node_name
        # The socket connection
        self.socket_connection = None

        # Threads to read and write to the socket connection
        self.incoming_thread = None
        self.outgoing_thread = None
        # Queues to safely communicate data between the threads
        self.incoming_queue: Queue = Queue()
        self.outgoing_queue: Queue = Queue()

        # Holds a reference to the parent context
        self.ctx = context

    def run(self):
        print("Starting: " + self.name)
        self.running = True
        while self.running:
            self.connect_to_server()

    def handle_message(self, msg):
        print(msg)

    def connect_to_server(self):
        # Create and configure the socket
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\n")
        # Loop around to establish connection while using timeout to allow for interruption
        while True:
            print("Attempting to connect....")

            self.socket_connection.connect((socket.gethostname(), 1234))

            print("\nConnection established\n\nWaiting for next message....\n")
            break

        # Loop around receiving and sending messages to the server

        try:
            print("Establishing connection with central server...")
            # Receive the central servers name
            msg_len = self.socket_connection.recv(4)
            msg_len = struct.unpack('i', msg_len)[0]
            self.central_server_name = self.socket_connection.recv(msg_len).decode("utf-8")

            # Send the name of the node
            msg_len = struct.pack('i', len(self.node_node))
            self.socket_connection.send(msg_len)
            self.socket_connection.send(bytes(self.node_node, "utf-8"))

            self.socket_connection.send(struct.pack('i', 0))
            # Start the incoming and outgoing threads
            self.incoming_thread = IncomingThread(self.node_node,
                                                  self.incoming_queue,
                                                  self.socket_connection)

            self.outgoing_thread = OutgoingThread(self.socket_connection,
                                                  self.node_node)

            self.ctx.is_connected = True
            while True:
                msg = self.incoming_queue.get()
                self.handle_message(msg)
        except KeyboardInterrupt:
            self.socket_connection.close()
            exit(0)

    def set_running(self, option: bool):
        self.running = option

    def break_down(self):
        print("Breaking down thread: " + self.name)
