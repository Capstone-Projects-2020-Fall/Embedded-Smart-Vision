import os
from _thread import start_new_thread

from ModuleMessage import ModuleMessage
from SocketConnection_Module.ConnectionThread import ConnectionThread
import time

from SocketConnection_Module.StreamingConnectionThread import StreamingConnectionThread
import cv2

class SocketClientModule:
    def __init__(self, conn):
        self.version = 1
        self.name = "socket client module"
        self.entry_point = self.__load__
        self.message_code = "SCM"

        self.conn = conn
        self.running = False

        # Tells us if the central server connection is established or not
        self.is_connected = False

        # noinspection PyTypeChecker
        self.main_connection_thread: ConnectionThread = ConnectionThread(context=self)
        self.streaming_connection_thread: StreamingConnectionThread = StreamingConnectionThread()

    def __proc_message__(self):
        # if we receive a message on the connection act on it
        if self.conn.poll():
            m = self.conn.recv()
            # Verify that the sender used the proper data type to send the message
            if isinstance(m, ModuleMessage):
                # Check if a message code exists for the given module
                ### HANDLE MESSAGES HERE ###
                if m.target == 'SCM' and m.tag == 'isConnected':
                    # Reply back with connection status
                    print('is connected')
                elif m.target == 'SCM' and m.tag == 'start_stream':
                    ## This is the condition for us to begin streaming
                    print("Starting up stream!")
                    start_new_thread(self.start_stream, ())
                elif m.target == 'SCM' and m.tag == 'update_stream_frame':
                    ## This handles incoming frames to be sent on the stream thread
                    print("Updating stream thread")
                    print("--Received Data--\n", m.message, "\n\n")
                    img = cv2.imdecode(m.message, cv2.IMREAD_COLOR)
                    

            else:
                print("Error! received unknown object as a message!")

    # This contains the actual operation of the module which will be run every time
    def __operation__(self):
        pass

    # Runs the modules functionality
    def __load__(self):
        running = True

        self.is_connected = False

        self.main_connection_thread.start()

        # While we are running do operations
        while running:
            self.__operation__()
            self.__proc_message__()

    # This function will start up the stream connection
    def start_stream(self):
        # Internal method to encapsulate repeated code
        def _start_stream():
            print("Starting new stream")

        if self.is_connected:
            _start_stream()
        else:
            while True:
                print("Node is not connected, waiting until connected")
                time.sleep(1)
                if self.is_connected:
                    print("Node connected")
                    _start_stream()
                    break


# Holder class to load the module in the old way
def __load__(conn):
    scm = SocketClientModule(conn)
    scm.__load__()
    print("Return from load call")


def __module_info__():
    module_info = {
        "version": 1,
        "name": "socket client module",
        "entry_point": __load__,
        # The code used to issue messages and establish pipes to the module
        "message_code": "SCM",
    }

    return module_info
