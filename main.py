import ModuleList
from multiprocessing import Process, Pipe
from _thread import *
from Config import cfg_transaction, Config, config_tags
import ModuleConnection
from time import sleep

# Actually starts up the process handling a given module and returns back the name followed by the process
from ModuleMessage import ModuleMessage

if __name__ == '__main__':
    # Our global variables, these are used to access state based information
    cfg: Config = Config()
    cfg.load_config()
    # Holds state information about our programming allowing us to get better communication of key states
    stateDict = {
        "connected": False,
        "stream_connected": False,
        "test": "This is test string"
    }


def get_state_value(key, reply=None):
    if key in stateDict:
        if reply is None:
            print("Error: attempting to get a variable without a reply pipe")
        else:
            reply.send(stateDict[key])
            reply.close()
    else:
        print("Requested state key was not found")
        if reply is None:
            print("Error: attempting to get a variable without a reply pipe")
        else:
            reply.send(None)
            reply.close()


def set_state_value(key, value):
    if key in stateDict:
        stateDict[key] = value
    else:
        print("set_state_value couldn't find key", key)


# Prints out the status of the running processes on an interval
def process_monitor(pool):
    while False:
        sleep(60)
        for p in pool:
            print(p, ":", pool[p].get('proc').is_alive())


def run_module(module_info):
    # print("Running module: ", module_info.get("name"))
    # Holds information about the name of the module
    n = module_info.get("name")

    # Create a pipe that will be passed for inter process communications between the modules
    # h for the host end
    # c for the child end
    h, c = Pipe(duplex=True)

    # Holds the process ID for the module
    # Create the new process targeting our entry point defined in the modules file
    p = Process(target=module_info.get("entry_point"), daemon=True, name=n, args=(c,))
    p.start()

    # Contains the info about the running process
    proc_info = {"proc": p, "pipe": h}
    return n, proc_info


# This is code that will be run once the program host has completed all tasks and is exiting
def break_down():
    print("Exiting program host!")


# Handles the inner-process communication calls
def message_handler(conns):
    for c in conns:
        # Check that we have data before attempting to recv data
        if conns[c].pipe.poll():
            # Receive the message to a temp variable
            m = conns[c].pipe.recv()
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
                    elif m.tag == 'get_state_data':
                        key, reply = m.message
                        get_state_value(key, reply)
                    elif m.tag == 'set_state_data':
                        key, value = m.message
                        set_state_value(key, value)
                # Check if a message code exists for the given module
                if m.target in conns:
                    conns[m.target].pipe.send(m)
                    # print(conns[m.target])
            else:
                print("Error! received unknown object as a message!")


# This function is the starting point for the program host
def start():
    # the list of modules we want to install
    module_list = ModuleList.module_list
    # will hold the process information
    process_pool = {}
    # A list of the modules connections to be passed as a parameter to the communication handler
    module_connections = {}
    for x in module_list:
        n, proc_info = run_module(x)
        process_pool[n] = proc_info
        Mconn = ModuleConnection.ModuleConnection(proc_info.get("pipe"), n)
        module_connections[x.get("message_code")] = Mconn

    # Create a pipe for the program host to send and receive data on
    host_pipe, send_end = Pipe(duplex=True)

    start_new_thread(process_monitor, (process_pool,))
    running = True
    while running:
        message_handler(module_connections)

    for p in process_pool:
        process_pool[p].get("proc").join()

    # print(module_connections)
    break_down()


if __name__ == '__main__':
    start()
