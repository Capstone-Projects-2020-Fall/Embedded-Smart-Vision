import os
from datetime import datetime

from ModuleMessage import ModuleMessage
from Classification_Module.Classifier import Classifier
import cv2 as cv

tagfile = open('Videos/TaggedVideos', 'w')
classifier = Classifier()

_Minfo = {
    "version": 1,
    "name": "Classification Module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "IPM",
}

recording = False
video_count = 0
last_found = datetime.now()
frames = list()


# Processes any messages left on the queue
def __proc_message__(conn):
    # if we receive a message on the connection act on it
    if conn.poll():
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            # Check if a message code exists for the given module
            ### HANDLE MESSAGES HERE ###
            if m.target == 'IPM' and m.tag == 'video':
                faces = m.message
                tags = classifier.apply_tags(faces)
                add_tags_message = ModuleMessage("WPM", "New Video Tags", tags)
                conn.send(add_tags_message)
                print('done classifying!')
            if m.target == 'IPM' and m.tag == 'New Frame':
                frame = m.message
                names = classifier.classify(frame)
                if len(names) > 0:
                    print(names)
        else:
            print("Error! received unknown object as a message!")

"""
def start_recording():
    global recording, frames, last_found
    if found:
        # Check who is in the frame
        classify_message = ModuleMessage("IPM", "New Frame", frame)
        conn.send(classify_message)
        # Add frame to video and document time face was last found
        last_found = datetime.now()
        frames.append(frame)
        faces.append(frame)
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


def stop_recording():
    global recording, frames, last_found
"""


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


# This contains the actual operation of the module which will be run every time
def __operation__():
    ### ADD MODULE OPERATIONS HERE ###
    pass


# Runs the modules functionality
def __load__(conn):
    # Make Directory for Videos
    path = os.path.join(os.getcwd(), 'Videos/')
    if not os.path.isdir(path):
        os.mkdir(path)

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
