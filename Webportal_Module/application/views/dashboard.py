# main_page.py
# import the necessary packages
import os
from flask import Blueprint, render_template, url_for, send_file
from ..models import Video, Tag


dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show_video():
    # rendering webpage
    video = Video.query.first()
    path = '/grabVideo/' + video.path
    print('Got following path: ' + path)
    return render_template('dashboard.html', video=path)


@dashboard.route('/grabVideo/<videoname>')
def grab_video(videoname):
    return send_file("C://Users/jimmy/PycharmProjects/Embedded-Smart-Vision/Videos/" + videoname)