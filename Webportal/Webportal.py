from multiprocessing.connection import PipeConnection

from ModuleCommunicationHandler.ModuleMessage import ModuleMessage

_Minfo = {
    "version": 1,
    "name": "Web portal",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "WPM",
}


# Processes any messages left on the queue
def __proc_message__(conn: PipeConnection):
    # if we receive a message on the connection act on it
    if conn.poll():
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            # Check if a message code exists for the given module
            ### HANDLE MESSAGES HERE ###
            print("User IO: ", m.message)
        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__():
    ### ADD MODULE OPERATIONS HERE ###
    pass


# Runs the modules functionality
def __load__(conn: PipeConnection):
    # Let the world know we are loading a new object
    setup_message = ModuleMessage("HIO",
                                  "loading",
                                  "Loading " + _Minfo["name"] + "...")
    conn.send(setup_message)

    # Let the world know we are loading a new object
    setup_message = ModuleMessage("HIO",
                                  "ready",
                                  _Minfo["name"] + " done loading!")
    conn.send(setup_message)
    running = True
    # While we are running do operations
    while running:
        __operation__()
        __proc_message__(conn)


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo
