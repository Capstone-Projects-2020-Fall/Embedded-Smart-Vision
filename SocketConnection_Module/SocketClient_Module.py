import os

from ModuleMessage import ModuleMessage
from SocketConnection_Module.ConnectionThread import ConnectionThread

_Minfo = {
    "version": 1,
    "name": "socket client module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "SCM",
}


# Processes any messages left on the queue
def __proc_message__(conn):
    # if we receive a message on the connection act on it
    if conn.poll():
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            # Check if a message code exists for the given module
            ### HANDLE MESSAGES HERE ###
            if m.target == 'SCM' and m.tag == 'isConnected':
                # Reply back with connection status
                print('done classifying!')
        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__(conn):
    pass


# Runs the modules functionality
def __load__(conn):
    running = True

    connected = False

    conn_thread: ConnectionThread = ConnectionThread()

    # While we are running do operations
    while running:
        __operation__(conn)
        __proc_message__(conn)


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo
