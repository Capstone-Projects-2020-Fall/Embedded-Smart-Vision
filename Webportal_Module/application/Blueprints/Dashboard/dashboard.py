# home_page.py
# import the necessary packages
from flask import Blueprint, render_template, Response
from ... import video_stream


dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show_live_video():
    return render_template('dashboard.html', current_page='dashboard')


def gen(stream):
    while True:
        frame = stream.get_current_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@dashboard.route('/videoFeed')
def video_feed():
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

