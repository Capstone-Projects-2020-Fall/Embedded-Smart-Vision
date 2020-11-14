# This class handles all the incoming traffic and messages
import struct
import threading
from queue import Queue
import socket

from SocketConnection_Module.IncomingThread import IncomingThread
from .OutgoingThread import OutgoingThread

import ProgramHostInterface as phi


class ConnectionThread(threading.Thread):

    def __init__(self, ipc_queue, node_name='UnnamedNode', context=None):
        """
        :param name:        The name of the thread
        :param inc_queue:   This queue will hold all of the incoming information, we should only be pushing to this
        :param connection:  The socket we are listening on
        """
        # Call the supers init function
        threading.Thread.__init__(self)
        self.name = 'Connection Thread'
        self.running = False
        self.central_server_name = None
        self.node_node = node_name

        # Holds a reference to the parent context
        self.ctx = context
        self.ipc_queue = ipc_queue

        # The socket connection
        self.socket_connection = None
        self.ip = ""
        self.port = 0
        # Threads to read and write to the socket connection
        self.incoming_thread = None
        self.outgoing_thread = None
        # Queues to safely communicate data between the threads
        self.incoming_queue: Queue = Queue()
        self.outgoing_queue: Queue = Queue()





    def run(self):
        print("Starting: " + self.name)
        self.running = True
        while self.running:
            self.connect_to_server()

        print("Returning from connection thread")

    def handle_message(self, msg):
        print(msg)

    def put_on_out_queue(self, data):
        print("Putting message on queue")
        self.outgoing_queue.put(data)

    def connect_to_server(self):
        # Create and configure the socket
        self.ip = phi.get_config_value(key="central_server_IP", prgh_queue=self.ipc_queue)
        self.port = int(phi.get_config_value(key="central_server_port", prgh_queue=self.ipc_queue))
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\n")
        # Loop around to establish connection while using timeout to allow for interruption
        while True:
            print("Attemping to connect to", self.ip + ":" + str(self.port))
            print(socket.gethostname())
            self.socket_connection.connect((self.ip, self.port))

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

            self.outgoing_thread = OutgoingThread(self.outgoing_queue,
                                                  self.socket_connection)

            self.outgoing_thread.start()

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
