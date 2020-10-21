from Camera_Module import Camera
import cv2 as cv
import os

cam = Camera.Camera()
count = 1

# Make Directory to Store Images
if not os.path.isdir('Images'):
    os.mkdir('Images')
while True:
    img = cam.grab_frame()
    Camera.show_image(img)
    path = 'Images/image%d.jpg' % count
    cropped_path = 'Images/face%d.jpg' % count
    Camera.save_image(img, path)

    #User needs to find path of the cascade classifier on their device and change the path until I figure out a solution to this issue
    cascade_face = cv.CascadeClassifier(r'C:\Users\Nick Sisko\Downloads\opencv\build\etc\haarcascades\haarcascade_frontalface_default.xml')
    cropped_image = Camera.face_detection(cascade_face, img)
    Camera.save_image(cropped_image, cropped_path)
    count += 1
    if cv.waitKey(1) & 0xFF == ord('e'):
        break

cam.__del__()

