# This is an interface for interacting directly with the program host
from multiprocessing.connection import Connection, Pipe

from Config import cfg_transaction
from ModuleMessage import ModuleMessage


class CFGT:
    def __init__(self):
        pass

    CFG_GET = "cfg_get"
    CFG_SET = "cfg_set"


def get_config_value(conn: Connection, key):
    h, c = Pipe(duplex=True)
    cfg_msg = cfg_transaction(key, is_set_var=False, reply=c)

    config_message = ModuleMessage("PRGH", CFGT.CFG_GET, cfg_msg)
    conn.send(config_message)

    msg = h.recv()
    print(msg)
    return msg
