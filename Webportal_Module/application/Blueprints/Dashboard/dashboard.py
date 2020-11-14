# home_page.py
# import the necessary packages
import base64
from flask import Blueprint, render_template, Response
from ... import video_stream
import cv2
from Webportal_Module.application import socketio, emit

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show_live_video():
    return render_template('dashboard.html', current_page='dashboard')


@socketio.on('new_frame')
def new_frame(image):
    print("Requested new frame")
    frame = video_stream.get_current_frame()
    _, enc = cv2.imencode('.jpg', frame)
    im_bytes = enc.tobytes()
    # im_b64 = base64.b64encode(im_bytes)
    emit('image', im_bytes)



def gen(stream):
    while True:
        frame = stream.get_current_frame()
        _, enc = cv2.imencode('.jpg', frame)[1]
        im_bytes = enc.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        socketio.emit('image', im_b64)

        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@dashboard.route('/videoFeed')
def video_feed():
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
