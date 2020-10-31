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
faces = list()

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
    frame, found, face = cam.grab_frame()

    success, image = cv.imencode('.jpg', frame)
    frame_message = ModuleMessage("WPM", "New Frame", image.tobytes())
    conn.send(frame_message)

    if found:
        # Add frame to video and document time face was last found
        last_found = datetime.now()
        frames.append(frame)
        faces.append(face)
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
                face_copy = faces.copy()
                frames.clear()
                faces.clear()
                start_new_thread(make_video, (frame_copy, face_copy, conn, ))
                recording = False


def make_video(frames: list, faces: list, conn):
    print('Making Video')
    global video_count
    video_count += 1
    path = os.path.join(os.getcwd(), 'Videos', 'video%d.mp4' % video_count)
    video = cv.VideoWriter(path, cv.VideoWriter_fourcc('a','v','c','1'), 10, (800, 550))
    for frame in frames:
        video.write(frame)
    video.release()

    #Upload video to database
    path = os.path.basename(path)
    tag = ('face',)
    add_video_message = ModuleMessage("WPM", "New Video Path", (os.path.basename(path), tag))
    conn.send(add_video_message)

    #Send faces to classify
    video_message = ModuleMessage('IPM', 'video', faces)
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

    update_video_count()

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


def update_video_count():
    global video_count

# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo


if __name__ == '__main__':
    cam = Camera.Camera()
    while True:
        __operation__(cam)
