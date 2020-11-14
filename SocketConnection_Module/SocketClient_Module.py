import os
from queue import Queue
from _thread import start_new_thread
from threading import Thread

from ModuleMessage import ModuleMessage
from SocketConnection_Module.ConnectionThread import ConnectionThread
import time
import ProgramHostInterface as phi
from SocketConnection_Module.StreamingConnectionThread import StreamingConnectionThread
from SocketConnection_Module.NetworkMessageInterface import NetworkMessageInterface


class SocketClientModule:
    def __init__(self, prgh_conn):
        self.version = 1
        self.name = "socket client module"
        self.entry_point = self.__load__
        self.message_code = "SCM"

        self.host_message_queue = Queue()

        self.prgh_conn = prgh_conn
        self.running = False

        # The text name of this node
        self.node_name = phi.get_config_value(self.prgh_conn, "node_name")
        # Tells us if the central server connection is established or not
        self.is_connected = False
        self.streaming_connected = False
        # noinspection PyTypeChecker
        self.main_connection_thread: ConnectionThread = \
            ConnectionThread(self.host_message_queue, node_name=self.node_name, context=self)
        # noinspection PyTypeChecker
        self.streaming_connection_thread: StreamingConnectionThread = None

        self.NMI = NetworkMessageInterface(self.main_connection_thread.put_on_out_queue)

    def __proc_message__(self):
        # if we receive a message on the connection act on it
        if self.prgh_conn.poll():
            m = self.prgh_conn.recv()
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
                    # img = cv2.imdecode(m.message, cv2.IMREAD_COLOR)
                    if self.streaming_connected:
                        if self.streaming_connection_thread is None:
                            raise Exception("ERROR: SocketClient_Module, the streaming"
                                            " thread is supposed to be connected but the thread was not set!")
                        else:
                            # if everything is all good we can attempt to update the frame
                            self.streaming_connection_thread.update_frame(m.message)
                    else:
                        print("Streaming server is not connected!")

                elif m.target == self.message_code and m.tag == 'network_message':
                    print("Handling network message")
                    ## We will handle this as a network message
                    self.NMI.handle_network_message(m.optional_tag, m.message)

                elif m.target == self.message_code and m.tag == 'shut_down':
                    print("Socket Client Module is shutting down")
                    self.running = False
            else:
                print("Error! received unknown object as a message!")

    # This contains the actual operation of the module which will be run every time
    def __operation__(self):
        if self.host_message_queue.qsize() > 0:
            msg = self.host_message_queue.get_nowait()
            self.prgh_conn.send(msg)

        if self.is_connected and not self.streaming_connected:
            self.start_stream()

    # Runs the modules functionality
    def __load__(self):
        running = True

        self.is_connected = False

        self.main_connection_thread.start()
        # We will start the stream by default
        # Thread(target=self.start_stream()).start()

        # While we are running do operations
        while running:
            self.__operation__()
            self.__proc_message__()

        self.__shut_down__()

    def __shut_down__(self):
        self.running = False
        quit()

    # This function will start up the stream connection
    def start_stream(self):
        # Internal method to encapsulate repeated code
        def _start_stream():
            print("Starting new stream")
            self.streaming_connection_thread = StreamingConnectionThread(self)
            self.streaming_connection_thread.start()
            self.streaming_connected = True

        if self.is_connected:
            _start_stream()
        else:
            print("Node is not connected, waiting until connected")
            time.sleep(1)
            if self.is_connected:
                print("Node connected")
                _start_stream()


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
