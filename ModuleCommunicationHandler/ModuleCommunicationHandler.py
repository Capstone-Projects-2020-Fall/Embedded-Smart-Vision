# This handles communication between the distinct modules that are currently running
from multiprocessing.connection import PipeConnection

from ModuleCommunicationHandler.ModuleMessage import ModuleMessage

_Minfo = {
    "version": 1,
    "name": "Module Communication Handler Module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "MCH",
}


# Processes any messages left on the queue
def __proc_message__(conns, host: PipeConnection):
    for c in conns:
        # Check that we have data before attempting to recv data
        if conns[c].pipe.poll():
            # Receive the message to a temp variable
            m = conns[c].pipe.recv()
            # Verify that the sender used the proper data type to send the message
            if isinstance(m, ModuleMessage):
                if m.target == "PRGH":
                    # This message is to be sent to the program host
                    host.send(m)
                # Check if a message code exists for the given module
                if m.target in conns:
                    conns[m.target].pipe.send(m)
                    print(conns[m.target])
            else:
                print("Error! received unknown object as a message!")


# Runs the modules functionality
def __load__(conns, host):

    while True:
        __proc_message__(conns, host)


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo
