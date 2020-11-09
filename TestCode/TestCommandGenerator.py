# This is a simple thread that just waits a given amount of
# time then raises a sequence of commands for other modules
import threading
from multiprocessing.connection import Connection
import time

# Handles the inner-process communication calls
from Config import cfg_transaction, config_tags, Config
from ModuleMessage import ModuleMessage

cfg = Config()
cfg.load_config()


def message_handler(conn):
    # Check that we have data before attempting to recv data
    if conn.poll():
        # Receive the message to a temp variable
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            if m.target == "PRGH":
                # This message is to be sent to the program host
                if m.tag == config_tags.CFG_SET:
                    # This message is attempting to access the config
                    if isinstance(m.message, cfg_transaction):
                        # Check our payload is the correct class type
                        prm: cfg_transaction = m.message
                        cfg.var_transaction(prm)
                    else:
                        print("Error in program host: attempted to update the config but passed bad data")
                elif m.tag == config_tags.CFG_GET:
                    if isinstance(m.message, cfg_transaction):
                        # Check our payload is the correct class type
                        prm: cfg_transaction = m.message
                        cfg.var_transaction(prm)
                    else:
                        print("Error in program host: attempted to update the config but passed bad data")

        else:
            print("Error! received unknown object as a message!")


class TestCommandThread(threading.Thread):

    def __init__(self, name="test-message-generator",
                 conn=None):
        threading.Thread.__init__(self)
        self.name = name
        self.conn = conn
        self.running = False

    def run(self):
        print("Starting" + self.name)
        self.running = True
        while self.running:
            message_handler(self.conn)

    def send_message(self, msg):
        self.conn.send(msg)
