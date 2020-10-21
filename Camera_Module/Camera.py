import cv2 as cv
import numpy as np
import os


def save_image(img: np.ndarray, path):
    cv.imwrite(path, img)


def show_image(img: np.ndarray):
    cv.imshow('frame', img)


class Camera:
    def __init__(self):
        self.cam = cv.VideoCapture(0)
        self.frame_size = (800, 550)
        path = os.path.join(os.getcwd(), '..', 'Webportal/static/video.mp4');
        self.video = cv.VideoWriter(path, 0, 30, self.frame_size)

    def __del__(self):
        self.cam.release()
        self.video.release()
        cv.destroyAllWindows()

    # Grabs frame from passed VideoCapture object (usb camera)
    def grab_frame(self) -> np.ndarray:
        ret, frame = self.cam.read()
        frame = cv.resize(frame, self.frame_size, interpolation=cv.INTER_NEAREST)
        norm = np.zeros(self.frame_size)
        norm = cv.normalize(frame, norm, 0, 255, cv.NORM_MINMAX)
        self.video.write(norm)
        return norm
