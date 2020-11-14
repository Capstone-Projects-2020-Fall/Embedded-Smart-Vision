# This is an interface for interacting directly with the program host
from multiprocessing.connection import Connection, Pipe

from Config import cfg_transaction
from ModuleMessage import ModuleMessage


class CFGT:
    def __init__(self):
        pass

    CFG_GET = "cfg_get"
    CFG_SET = "cfg_set"


def get_config_value(conn: Connection = None, key=None, prgh_queue=None):
    print("ProgramHostInterface - requesting data: ", key)
    h, c = Pipe(duplex=True)
    cfg_msg = cfg_transaction(key, is_set_var=False, reply=c)

    config_message = ModuleMessage("PRGH", CFGT.CFG_GET, cfg_msg)
    if conn is not None:
        conn.send(config_message)
    elif prgh_queue is not None:
        prgh_queue.put(config_message)
    else:
        raise Exception("get_config_value() was called without a pipe or queue")

    msg = h.recv()
    print(msg)
    return msg
