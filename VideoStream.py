import os


class Stream(object):
    def __init__(self):
        self.count = 0

    def get_frame(self):
        path = 'Images/image%d.jpg' % self.count
        if os.path.isfile(path):
            self.count += 1
            return open(path, 'rb').read()
        else:
            self.count = 1
            return self.get_frame()
