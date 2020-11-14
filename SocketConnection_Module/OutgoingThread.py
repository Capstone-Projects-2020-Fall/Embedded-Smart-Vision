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
                self.send_video_to_server(message.var1, message.var2)

    # Sends a given video link to the central server
    def send_video_to_server(self, path, tags):
        # TODO type check path and tags
        # Send the actual video to the server
        # Open the video in the path
        cap = cv2.VideoCapture(path)

        # Check to make sure we opened the video file properly
        if cap.isOpened() is False:
            # Send a -1 to the server telling it that the video upload failed
            self.socket_conn.sendall(struct.pack('i', -1))
            raise Exception("Failed to open video to send to server")

        ### File Success Check ###
        self.socket_conn.sendall(struct.pack('i', 1))

        print("OutgoingThread - tags count:", len(tags))
        ### Tag Count ###
        self.socket_conn.sendall(struct.pack('i', len(tags)))

        # Per Tag Interaction #
        for t in tags:
            # TODO type check tags to make sure only strings were sent
            print("Sending tag: ", t)
            tag_bytes = bytes(t, "utf-8")
            ### Length of tag ###
            self.socket_conn.sendall(struct.pack('i', len(tag_bytes)))
            ### Tag Bytes ###
            self.socket_conn.sendall(tag_bytes)

        ### Tags done ###
        self.socket_conn.sendall(struct.pack('i', -1))

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        ### Send Frame Count ###
        self.socket_conn.sendall(struct.pack('i', frame_count))

        ### Send width and height ###
        self.socket_conn.sendall(struct.pack('ii', frame_width, frame_height))

        # For each frame #
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                # Process the video and send the frame
                data = pickle.dumps(frame)
                # pickle.dumps(frame)
                # Pack up and send the length of our frame follow by the frame data
                ### frame size and frame data ###
                self.socket_conn.sendall(struct.pack('I', len(data)) + data)

            else:
                ### confirm end of frames ###
                self.socket_conn.sendall(struct.pack('i', -1))
                break
