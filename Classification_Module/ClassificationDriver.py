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
face_detector = cv.CascadeClassifier('Camera_Module/face_data.xml')


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
                desired_face_found = False
                frame = m.message
                face_locations = detect_faces(frame)
                global last_found, tags
                if len(face_locations) > 0:
                    names = classifier.classify(frame, face_locations)
                    # Record when last face was found
                    last_found = datetime.now()
                    # Tell camera to start recording if it isn't already
                    record_message = ModuleMessage("CM", "Start Recording", None)
                    conn.send(record_message)
                    # Add classified names to our list
                    for name in names:
                        tags.add(name)
                        led_on_message = ModuleMessage("ACT", "Face Found", None)
                        conn.send(led_on_message)
                        #print(name)
                        desired_face_found = True
                else:
                    # No face found for too long, so stop recording if we are recording
                    now = datetime.now()
                    delta = now - last_found
                    if delta.seconds > 2:
                        if len(tags) == 0:
                            tags.add('Unknown Person')
                        stop_record_message = ModuleMessage("CM", "Stop Recording", tags)
                        conn.send(stop_record_message)
                        tags.clear()
                if desired_face_found is False:
                    led_off_message = ModuleMessage("ACT", "Face Not Found", None)
                    conn.send(led_off_message)
        else:
            print("Error! received unknown object as a message!")


def detect_faces(image):
    image_copy = image.copy()
    grayscale = cv.cvtColor(image_copy, cv.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5)
    face_locations = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
    return face_locations


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
