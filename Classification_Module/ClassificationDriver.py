import os
from datetime import datetime

from ModuleMessage import ModuleMessage
from Classification_Module.Classifier import Classifier
import cv2 as cv

classifier = Classifier()

_Minfo = {
    "version": 1,
    "name": "Classification Module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "IPM",
}

last_found = datetime.now()
tags = set()


# Processes any messages left on the queue
def __proc_message__(conn):
    # if we receive a message on the connection act on it
    if conn.poll():
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            # Check if a message code exists for the given module
            ### HANDLE MESSAGES HERE ###
            """
            if m.target == 'IPM' and m.tag == 'video':
                faces = m.message
                tags = classifier.apply_tags(faces)
                add_tags_message = ModuleMessage("WPM", "New Video Tags", tags)
                conn.send(add_tags_message)
                print('done classifying!')
            """
            if m.target == 'IPM' and m.tag == 'New Frame':
                frame = m.message
                names = classifier.classify(frame)
                global last_found, tags
                if len(names) > 0:
                    # Record when last face was found
                    last_found = datetime.now()
                    # Tell camera to start recording if it isn't already
                    record_message = ModuleMessage("CM", "Start Recording", None)
                    conn.send(record_message)
                    # Add classified names to our list
                    for name in names:
                        tags.add(name)
                else:
                    # No face found for too long, so stop recording if we are recording
                    now = datetime.now()
                    delta = now - last_found
                    if delta.seconds > 2:
                        stop_record_message = ModuleMessage("CM", "Stop Recording", tags)
                        conn.send(stop_record_message)
                        tags.clear()

        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__():
    ### ADD MODULE OPERATIONS HERE ###
    pass


# Runs the modules functionality
def __load__(conn):
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
    face = cv.imread('Images/face6.jpg')
    classification = classifier.classify(face)
    print(classification)
