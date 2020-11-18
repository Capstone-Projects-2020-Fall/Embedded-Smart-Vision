# This is an interface for creating messages to be send to the socket connection module
from multiprocessing.connection import Connection

from ModuleMessage import ModuleMessage
import cv2

scm = "SCM"


def start_stream_message(conn: Connection):
    add_video_message = ModuleMessage(scm, "start_stream", "contents")
    conn.send(add_video_message)


# Sends a message to the socket client updating the latest frame
def update_stream_frame(conn: Connection, image):
    frame_message = ModuleMessage(scm, 'update_stream_frame', image)
    conn.send(frame_message)


# Send a test message over the network
def send_test_message(conn: Connection, text):
    msg = ModuleMessage(scm, 'network_message', text, optional_tag='send_test_message')
    conn.send(msg)


def send_video_file(conn: Connection, path, tags):
    msg = ModuleMessage(scm, 'network_message', (path, tags), optional_tag='send_video')
    conn.send(msg)


def shut_down_module(conn: Connection):
    msg = ModuleMessage(scm, 'shut_down', "")
    conn.send(msg)
