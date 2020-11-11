import os

import cv2 as cv
import numpy as np


def save_image(img, path):
    cv.imwrite(path, img)


def show_image(img):
    cv.imshow('frame', img)


def detect_face(cascade, image):
    image_copy = image.copy()
    grayscale = cv.cvtColor(image_copy, cv.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5)
    if len(faces) > 0:
        face_found = True
    else:
        face_found = False

    return face_found


class Camera:
    def __init__(self):
        self.cam = cv.VideoCapture(0)
        self.frame_size = (800, 550)
        self.cascade = cv.CascadeClassifier('Camera_Module/face_data.xml')
        self.recording = False

    def __del__(self):
        self.cam.release()
        cv.destroyAllWindows()

    # Grabs frame from passed VideoCapture object (usb camera)
    def grab_frame(self):
        ret, frame = self.cam.read()
        frame = cv.resize(frame, self.frame_size, interpolation=cv.INTER_NEAREST)
        norm = np.zeros(self.frame_size)
        norm = cv.normalize(frame, norm, 0, 255, cv.NORM_MINMAX)
        #found = detect_face(self.cascade, norm)
        return norm
