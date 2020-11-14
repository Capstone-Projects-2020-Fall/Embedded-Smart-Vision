import threading
from multiprocessing import Pipe
from queue import Queue

from ModuleMessage import ModuleMessage
from Webportal_Module.application import create_app, DBInterface, video_stream

_Minfo = {
    "version": 1,
    "name": "Web portal",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "WPM",
}

videoIDs = Queue(0)


# Processes any messages left on the queue
def __proc_message__(conn):
    global path, tags
    # if we receive a message on the connection act on it
    if conn.poll():
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            # Check if a message code exists for the given module
            ### HANDLE MESSAGES HERE ###
            if m.target == "WPM" and m.tag == 'New Frame':
                video_stream.update_frame(m.message)
            if m.target == "WPM" and m.tag == "New Video Path":
                path = m.message[0]
                tags = m.message[1]
                videoID = DBInterface.add_video(path, tags)
                videoIDs.put(videoID)
            if m.target == "WPM" and m.tag == "New Video Tags":
                tags = m.message
                DBInterface.add_tags(videoIDs.get(), tags)
        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__(conn):
    ### ADD MODULE OPERATIONS HERE ###
    socketio, app = create_app()
    message_thread = threading.Thread(target=check_messages, args=(app, conn,), daemon=True)
    message_thread.start()
    socketio.run(app)


def check_messages(app, conn):
    app.app_context().push()
    """
    parent_path = os.path.join(os.pardir, 'Videos')
    videos = os.listdir(parent_path)
    count = 1
    for video in videos:
        tag = 'Tag%d' % count
        DBInterface.add_video(video, (tag,))
        count += 1
    from Webportal_Module.application.models import Tag, Video
    tags = Tag.query.all()
    for tag in tags:
        print(tag.videoID, tag.classification)
    videos = Video.query.all()
    for video in videos:
        print(video.path)
    """
    while True:
        __proc_message__(conn)


# Runs the modules functionality
def __load__(conn):

    # While we are running do operations
    __operation__(conn)


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo


if __name__ == '__main__':
    app = create_app()
    app.run()
