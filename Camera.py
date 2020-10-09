import cv2 as cv
import numpy as np


def save_image(img: np.ndarray, path):
    cv.imwrite(path, img)


def show_image(img: np.ndarray):
    cv.imshow('frame', img)


class Camera:
    def __init__(self):
        self.cam = cv.VideoCapture(0)

    def __del__(self):
        self.cam.release()
        cv.destroyAllWindows()

    # Grabs frame from passed VideoCapture object (usb camera)
    def grab_frame(self) -> np.ndarray:
        ret, frame = self.cam.read()
        norm = np.zeros((800, 550))
        norm = cv.normalize(frame, norm, 0, 255, cv.NORM_MINMAX)
        return norm
