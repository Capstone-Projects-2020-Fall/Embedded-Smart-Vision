from ModuleMessage import ModuleMessage

from Camera_Module import Camera
import cv2 as cv
import numpy as np
import os
from _thread import start_new_thread
from queue import Queue

baseline_frame = np.zeros((0, 1))
frames = list()
recording = False
video_writers = Queue()
current_video_writer: cv.VideoWriter = None
video_directory = os.path.join(os.getcwd(), 'Videos')
video_count = len(os.listdir(video_directory))
path = os.path.join(video_directory, 'video%d.mp4' % video_count)
messages = Queue(0)

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
            if m.target == 'CM' and m.tag == 'Start Recording':
                if not recording:
                    start_recording()
                else:
                    pass
            if m.target == 'CM' and m.tag == 'Stop Recording':
                if recording:
                    tags = m.message
                    stop_recording(tags)
                else:
                    pass
        else:
            print("Error! received unknown object as a message!")


def start_recording():
    global recording, current_video_writer, video_directory, path, video_count
    recording = True
    current_video_writer = cv.VideoWriter(path, cv.VideoWriter_fourcc('a', 'v', 'c', '1'), 10, (800, 550))
    video_writers.put(current_video_writer)
    #print("Started Recording")


def stop_recording(tags: set):
    #print("Stopping Recording")
    global recording, path, video_count
    start_new_thread(upload_video, (tags, path, ))
    video_count = video_count + 1
    path = os.path.join(video_directory, 'video%d.mp4' % video_count)
    recording = False


def upload_video(tags, video_path):
    global video_writers
    video = video_writers.get()
    video.release()
    add_video_message = ModuleMessage("WPM", "New Video Path", (os.path.abspath(video_path), tags))
    messages.put(add_video_message)


# This contains the actual operation of the module which will be run every time
def __operation__(cam: Camera.Camera, conn):
    ### ADD MODULE OPERATIONS HERE ###
    # Grab Frame from camera
    frame = cam.grab_frame()
    if recording:
        current_video_writer.write(frame)

    # Send frame to webportal live feed
    success, image = cv.imencode('.jpg', frame)
    frame_message = ModuleMessage("WPM", "New Frame", frame)
    conn.send(frame_message)

    frame_message = ModuleMessage("SCM", "update_stream_frame", frame)
    conn.send(frame_message)

    # Send frame to be classified if motion was detected
    global baseline_frame
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame = cv.GaussianBlur(gray_frame, (25, 25), 0)

    delta = cv.absdiff(baseline_frame, gray_frame)
    threshold = cv.threshold(delta, 35, 255, cv.THRESH_BINARY)[1]

    (contours, _) = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        # Motion detected, so send frames to be classified
        frame_message = ModuleMessage("IPM", "New Frame", frame)
        conn.send(frame_message)
        baseline_frame = gray_frame
    else:
        # No motion detected; do nothing
        pass


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

    # Create a camera object
    cam = Camera.Camera()

    global baseline_frame
    baseline_frame = cam.grab_frame()
    baseline_frame = cv.cvtColor(baseline_frame, cv.COLOR_BGR2GRAY)
    baseline_frame = cv.GaussianBlur(baseline_frame, (25, 25), 0)

    running = True
    # While we are running do operations
    while running:
        # Send any video path messages to the Web portal
        while not messages.empty():
            conn.send(messages.get())

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
