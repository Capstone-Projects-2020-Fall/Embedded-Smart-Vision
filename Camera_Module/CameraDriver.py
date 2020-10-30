import os
from _thread import start_new_thread
from multiprocessing import connection
from datetime import datetime, timedelta

from ModuleMessage import ModuleMessage

from Camera_Module import Camera
import cv2 as cv
import numpy as np

recording = False
video_count = 0
last_found = datetime.now()
frames = list()

_Minfo = {
    "version": 1,
    "name": "Camera Module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "CM",
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
            print("User IO: ", m.message)
        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__(cam: Camera.Camera, conn):
    ### ADD MODULE OPERATIONS HERE ###
    # Grab Frame and check if face was found
    global recording, frames, last_found
    frame, found = cam.grab_frame()

    success, frame = cv.imencode('.jpg', frame)
    frame_message = ModuleMessage("WPM", "New Frame", frame.tobytes())
    conn.send(frame_message)

    if found:
        # Add frame to video and document time face was last found
        last_found = datetime.now()
        frames.append(frame)
        # Start Recording if we aren't already
        if not recording:
            recording = True
            print('starting recording')
    else:
        if recording:
            # Add frame because we're recording
            frames.append(frame)
            current_time = datetime.now()
            delta = current_time - last_found
            # Face has not been present for too long, sto stop recording
            if delta.seconds > 3:
                frame_copy = frames.copy()
                frames.clear()
                start_new_thread(make_video, (frame_copy, conn, ))
                recording = False


def make_video(frames: list, conn):
    print('Making Video')
    global video_count
    video_count += 1
    path = os.path.join(os.getcwd(), 'Videos', 'video%d.mp4' % video_count)
    video = cv.VideoWriter(path, 0, 10, (800, 550))
    for frame in frames:
        video.write(frame)
    video.release()
    video_message = ModuleMessage('IPM', 'video', os.path.abspath(path))
    conn.send(video_message)


# Runs the modules functionality
def __load__(conn):
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

    #Make Directory for Videos
    path = os.path.join(os.getcwd(), 'Videos/')
    if not os.path.isdir(path):
        os.mkdir(path)

    # Create a camera object
    cam = Camera.Camera()

    running = True
    # While we are running do operations
    while running:
        __operation__(cam, conn)
        __proc_message__(conn)

    cam.__del__()


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo


if __name__ == '__main__':
    cam = Camera.Camera()
    while True:
        __operation__(cam)
