import cv2 as cv
import numpy as np


def save_image(img: np.ndarray, path):
    cv.imwrite(path, img)


def show_image(img: np.ndarray):
    cv.imshow('frame', img)

def face_detection(cascade, image):
    image_copy = image.copy()
    grayscale = cv.cvtColor(image_copy, cv.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(grayscale, scaleFactor = 1.1, minNeighbors = 5)

    for (x, y, w, h) in faces:
        cv.rectangle(image_copy, (x,y), (x+w, y+h), (0, 255, 0), 15)
    crop_image = image_copy[y: y+h, x: x+w]
    return crop_image

class Camera:
    def __init__(self):
        self.cam = cv.VideoCapture(0)
        self.frame_size = (800, 550)
        self.video = cv.VideoWriter('static/video.mp4', 0, 30, self.frame_size)

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



