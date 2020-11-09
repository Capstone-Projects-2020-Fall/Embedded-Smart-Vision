# This class handles all the outgoing traffic and messages
import pickle
import struct
import threading

import cv2

from SocketConnection_Module.NetworkSendMessage import NetworkSendMessage, NSM_TYPE


class OutgoingThread(threading.Thread):

    def __init__(self, queue, conn):
        threading.Thread.__init__(self)
        self.message_queue = queue
        self.socket_conn = conn
        self.running = False
        self.name = 'Outgoing Thread'

    def run(self):
        print("Starting" + self.name)
        self.running = True
        while self.running:
            print("Waiting for next message")
            message = self.message_queue.get()
            print("Found message on queue")
            # Check that we are putting the proper messages onto the queue
            if not isinstance(message, NetworkSendMessage):
                raise TypeError("The last message retrieved from the outgoing queue was not the correct data type")

            if message.message_type == NSM_TYPE.INVALID:
                raise Exception("The message must not have been initialized before being put in the queue")
            elif message.message_type == NSM_TYPE.TEST_MESSAGE:
                print("Sending test message!")
                # Test message to verify messages are sending properly
                # Send the message type
                self.socket_conn.sendall(struct.pack('i', NSM_TYPE.TEST_MESSAGE))
                # Send whatever string is in var1
                data = bytes(message.var1, 'utf-8')
                msg_len = struct.pack('I', len(data))
                self.socket_conn.sendall(msg_len)
                self.socket_conn.sendall(data)
            elif message.message_type == NSM_TYPE.SEND_VIDEO:
                ## We want to take the data in this message and send the video to the server
                self.socket_conn.sendall(struct.pack('i', NSM_TYPE.SEND_VIDEO))
                self.send_video_to_server(message.var1)

    # Sends a given video link to the central server
    def send_video_to_server(self, link):
        cap = cv2.VideoCapture(link)

        if cap.isOpened() is False:
            raise Exception("Failed to open video to send to server")

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        self.socket_conn.sendall(struct.pack('ii', frame_width, frame_height))
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                # Process the video and send the frame
                data = pickle.dumps(frame)
                # pickle.dumps(frame)
                # Pack up and send the length of our frame follow by the frame data
                self.socket_conn.sendall(struct.pack('I', len(data)) + data)

            else:
                self.socket_conn.sendall(struct.pack('i', 0))
                break
