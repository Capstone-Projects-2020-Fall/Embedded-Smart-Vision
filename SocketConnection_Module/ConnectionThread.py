# This class handles all the incoming traffic and messages
import struct
import threading
from queue import Queue
from socket import socket
from MessagePack import MessagePack, MsgType, get_bytes, Header


class ConnectionThread(threading.Thread):

    def __init__(self):
        """
        :param name:        The name of the thread
        :param inc_queue:   This queue will hold all of the incoming information, we should only be pushing to this
        :param connection:  The socket we are listening on
        """
        # Call the supers init function
        threading.Thread.__init__(self)
        self.running = False
        self.central_server_name = None

        # The socket connection
        self.socket_connection = None

        # Threads to read and write to the socket connection
        self.incoming_thread = None
        self.outgoing_thread = None
        # Queues to safely communicate data between the threads
        self.incoming_queue = None
        self.outgoing_queue = None

    def run(self):
        print("Starting: " + self.name)
        self.running = True
        while self.running:
            pass

    def connect_to_server(self):
        # Create and configure the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\n")
        # Loop around to establish connection while using timeout to allow for interruption
        while True:
            print("Attempting to connect....")
            try:
                s.connect((socket.gethostname(), 1234))
            except socket.timeout:
                continue

            print("\nConnection established\n\nWaiting for next message....\n")
            break

        # Loop around receiving and sending messages to the server

        try:
            print("Establishing connection with central server...")
            msg_len = s.recv(4)
            msg_len = struct.unpack('i', msg_len)[0]
            self.central_server_name = s.recv(msg_len).decode("utf-8")
            print("RECEIVED - Central server name: ", central_server_name)
            print("SENDING - Node Client Name: ", node_name)
            msg_len = struct.pack('i', len(node_name))
            s.send(msg_len)
            s.send(bytes(node_name, "utf-8"))

            msg = MessagePack(message_type=MsgType.COMMAND)
            str_cmd = StreamCommand(StreamCommand.START_STREAM)
            msg.set_data(str_cmd)

            byte_data = msg.create_byte_array()
            s.sendall(byte_data)

        except KeyboardInterrupt:
            s.close()
            exit(0)

    def set_running(self, option: bool):
        self.running = option

    def break_down(self):
        print("Breaking down thread: " + self.name)
