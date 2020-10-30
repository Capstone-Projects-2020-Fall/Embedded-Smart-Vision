import os
from datetime import datetime


class VideoStream(object):
    def __init__(self):
        default_frame_path = 'Webportal_Module/application/VideoStream/CameraOffline.jpg'
        self.default_frame = open(default_frame_path, 'rb').read()
        self.current_frame = self.default_frame
        self.last_updated = datetime.now()

    def get_current_frame(self):
        # Checks if frame has not been updated in over a second
        # If so, switches to default frame that alerts user their camera is offline
        now = datetime.now()
        time_delta = now - self.last_updated
        if time_delta.seconds > 1:
            self.current_frame = self.default_frame

        return self.current_frame

    def update_frame(self, frame):
        self.current_frame = frame
        self.last_updated = datetime.now()