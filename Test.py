import Camera
import cv2 as cv

cam = Camera.Camera()
count = 1
while True:
    img = cam.grab_frame()
    Camera.show_image(img)
    path = 'Images/image%d.jpg' % count
    Camera.save_image(img, path)
    count += 1
    if cv.waitKey(1) & 0xFF == ord('e'):
        break

cam.__del__()