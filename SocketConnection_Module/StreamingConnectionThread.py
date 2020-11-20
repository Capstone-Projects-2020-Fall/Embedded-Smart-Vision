# this thread takes care of all the streaming business
import pickle
import socket
import struct
import threading
from queue import Queue
import time
import cv2
import numpy as np


class StreamingConnectionThread(threading.Thread):

    def __init__(self, context, central_ip, central_port):
        threading.Thread.__init__(self)
        self.name = 'Streaming Connection Thread'
        # Holds the latest frame
        self.latest_frames = Queue()
        self.running = False
        # Our parent context
        self.ctx = context
        # The connection to the central server
        self.conn = None
        self.central_ip = central_ip
        self.central_port = central_port

    def run(self):
        print("Starting" + self.name + " as a streaming thread")
        self.running = True

        # connect to the central server
        self.connect_central()

        while self.running:
            # Create a running loop
            # Block until we can get something from the queue
            # TODO time out the get request and show a default image if the queue has timed out
            frame = self.latest_frames.get()
            # print(type(frame))
            # Check if the streaming server is connected
            if self.ctx.streaming_server_is_connected:
                # Pickle our data to get a byte array
                data = cv2.imencode('.jpg', frame)[1].tobytes()
                
                # Pack up and send the length of our frame follow by the frame data
                msg_len = struct.pack('i', len(data))
                self.conn.sendall(msg_len)
                self.conn.sendall(data)
                time.sleep(1/24)

    # Connect to the central server
    def connect_central(self):
        # Create the socket and attempt to connect to the central server
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.central_ip, self.central_port))

        print("Streaming server established connection with central")

        # First step of the handshake is to receive the central servers name
        # Receive the length of the central servers name and decode it
        msg_len = struct.unpack('i', self.conn.recv(4))[0]
        # Receive and decode the name of the central server
        central_server_name = self.conn.recv(msg_len).decode("utf-8")

        # calculate the size of our name and convert it to a byte array
        name_bytes = bytes(self.ctx.node_name, 'utf-8')
        msg_len = struct.pack('i', len(name_bytes))
        # send the length of our name
        self.conn.sendall(msg_len)
        # Send out name bytes
        self.conn.sendall(name_bytes)
        # Tell the central server this is a streaming node
        stream_mode = 1
        self.conn.sendall(struct.pack('i', stream_mode))

        # Make a print out and then set our status to connected
        print("Handshake for streaming complete")
        self.ctx.streaming_server_is_connected = True

    # Update the latest frame being sent to the streaming server
    def update_frame(self, frame):
        self.latest_frames.put(frame)
