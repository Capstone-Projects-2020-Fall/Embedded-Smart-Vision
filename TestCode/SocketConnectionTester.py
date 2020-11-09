# This is functions that can be used to test the socket connection module
import time

import SocketConnection_Module.SocketClient_Module as scm
from multiprocessing import Process, Pipe
from SocketConnection_Module import Socket_Connection_Module_interface as scmi
import cv2

# This function will attempt to post a connection to the central server
from ModuleMessage import ModuleMessage


def start_socket_connection_module():
    send_pipe, host_pipe = Pipe(duplex=True)
    p = Process(target=scm.__load__, daemon=True, name="n", args=(send_pipe,))
    p.start()
    return host_pipe


def test_client_connection():
    p = start_socket_connection_module()
    scmi.start_stream_message(p)

    while True:
        pass


def test_send_frame_message_to_scm():
    p = start_socket_connection_module()
    # Open a test image using cv2
    test_image = cv2.imread('TestPhoto.jpg')
    success, to_send = cv2.imencode('.jpg', test_image)

    scmi.start_stream_message(p)

    time.sleep(2)
    scmi.update_stream_frame(p, to_send)

    while True:
        pass


if __name__ == '__main__':
    test_send_frame_message_to_scm()
