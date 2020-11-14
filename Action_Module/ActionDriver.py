import os
from datetime import datetime
from sys import platform

from ModuleMessage import ModuleMessage
if platform == "linux" or platform == "linux2":
    import RPi.GPIO as GPIO
elif platform == "win32":
    # If we have any windows specific code put it here
    pass

from time import sleep

on = False

_Minfo = {
    "version": 1,
    "name": "Action Module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "ACT",
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
            global on
            if m.target == 'ACT' and m.tag == 'Face Found':
                if on is False:
                    if platform == "linux" or platform == "linux2":
                        GPIO.output(18, True)
                    on = True
            if m.target == 'ACT' and m.tag == 'Face Not Found':
                if on is True:
                    if platform == "linux" or platform == "linux2":
                        GPIO.output(18, False)
                    on = False
        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__():
    ### ADD MODULE OPERATIONS HERE ###
    pass


# Runs the modules functionality
def __load__(conn):
    if platform == "linux" or platform == "linux2":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
    running = True
    # While we are running do operations
    while running:
        #__operation__()
        __proc_message__(conn)


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    while True:
        if on is True:
            GPIO.output(18, False)
            on = False
        else:
            GPIO.output(18, True)
            on = True
        sleep(1)
