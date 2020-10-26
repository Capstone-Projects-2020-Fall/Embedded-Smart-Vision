# main_page.py
# import the necessary packages
import os
from flask import Blueprint, render_template, url_for, send_file
from ..models import Video, Tag
from .. import video_directory

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.route('/dashboard')
def show_live_video():
    # rendering webpage
    video = Video.query.first()
    path = '/grabVideo/' + video.path
    print('Got following path: ' + path)
    return render_template('dashboard.html', video=path)
