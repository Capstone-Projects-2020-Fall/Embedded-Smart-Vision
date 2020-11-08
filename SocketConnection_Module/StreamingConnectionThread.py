# this thread takes care of all the streaming business
import threading


class StreamingConnectionThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("Starting" + self.name + " as a streaming thread")

