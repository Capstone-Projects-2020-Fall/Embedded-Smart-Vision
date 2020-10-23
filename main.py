import ModuleList
from multiprocessing import Process, Pipe

from Config import cfg_update, Config
from ModuleCommunicationHandler import ModuleCommunicationHandler
from ModuleCommunicationHandler import ModuleConnection


# Actually starts up the process handling a given module and returns back the name followed by the process
from ModuleCommunicationHandler.ModuleMessage import ModuleMessage


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


# This function is the starting point for the program host
def start():
    # Our global variables, these are used to access state based information
    cfg: Config = Config()
    cfg.load_config()

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

    # Setup the module communication handler
    # (We do this without actually installing the module because we want to make sure
    # it has the list of other modules since it is special)
    communication_handler = Process(target=ModuleCommunicationHandler.__load__,
                                    daemon=True,
                                    name="Module Communication Handler",
                                    args=(module_connections,send_end))
    communication_handler.start()

    running = True
    while running:
        # Wait for any messages to be sent
        message: ModuleMessage = host_pipe.recv()
        if message.tag == "cfg":
            # This message is attempting to access the config
            if isinstance(message.message, cfg_update):
                # Check our payload is the correct class type
                prm: cfg_update = message.message
                cfg.set_var(prm)
            else:
                print("Error in program host: attempted to update the config but passed bad data")

    for p in process_pool:
        process_pool[p].get("proc").join()

    communication_handler.join()
    # print(module_connections)
    break_down()


if __name__ == '__main__':
    start()
