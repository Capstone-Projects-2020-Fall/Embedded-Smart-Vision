# This class handles all the outgoing traffic and messages
import threading


class OutgoingThread(threading.Thread):

    def __init__(self, queue, conn):
        threading.Thread.__init__(self)
        self.message_queue = queue
        self.socket_conn = conn

    def run(self):
        print("Starting" + self.name)

        while True:
            message = self.message_queue.get()
            self.socket_conn.sendall(message)

