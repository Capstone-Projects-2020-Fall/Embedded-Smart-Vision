# This is an interface for creating messages to be send to the socket connection module
from multiprocessing.connection import PipeConnection, Connection

from ModuleMessage import ModuleMessage
import cv2


def start_stream_message(conn: Connection):
    add_video_message = ModuleMessage("SCM", "start_stream", "contents")
    conn.send(add_video_message)


# Sends a message to the socket client updating the latest frame
def update_stream_frame(conn: Connection, image):
    frame_message = ModuleMessage("SCM", 'update_stream_frame', image)
    conn.send(frame_message)
