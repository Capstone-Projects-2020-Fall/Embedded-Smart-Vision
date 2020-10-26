# import the necessary packages
from base64 import b64encode

from flask import Blueprint, render_template, send_file
from ..models import Video, Tag
from .. import video_directory
import cv2 as cv
from PIL import Image
import io

video_gallery = Blueprint('video_gallery', __name__,
                          template_folder='templates/video_gallery',
                          static_folder='gallery_static')


@video_gallery.route('/videoGallery')
def show_videos():
    videos = Video.query.all()
    tagged_videos = list()
    for video in videos:
        video_path = video.path
        tags = Tag.query.filter_by(videoID=video.id).all()
        video_with_tag = VideoWithTag(video_path, tags)
        tagged_videos.append(video_with_tag)
    return render_template('gallery.html', taggedVideos=tagged_videos)


@video_gallery.route('/grabVideo/<videoname>')
def grab_video(videoname):
    # print('Attempting to grab this video: ' + video_directory + videoname)
    return send_file(video_directory + videoname)

@video_gallery.route('/watchVideo/<videoname>')
def watch_video(videoname):
    path = '/grabVideo/' + videoname
    return render_template('video.html', tags='example', video=path)


class VideoWithTag:

    def __init__(self, path, tags):
        self.path = path

        self.tags = ''
        for tag in tags:
            self.tags = self.tags + tag.classification + ', '
        self.tags = self.tags[0:len(self.tags) - 2]

        size = 100, 100
        video = cv.VideoCapture(video_directory + path)
        video_length = int(video.get(cv.CAP_PROP_FRAME_COUNT)) - 1
        if video.isOpened() and video_length > 0:
            success, thumbnail = video.read()
            thumbnail = cv.cvtColor(thumbnail, cv.COLOR_BGR2RGB)
            thumbnail = Image.fromarray(thumbnail)
            thumbnail.thumbnail(size)
            # Following Code from https://stackoverflow.com/questions/59581565/how-to-display-flask-image-to-html-directly-without-saving
            file_object = io.BytesIO()
            thumbnail.save(file_object, 'JPEG')
            self.image = "data:image/jpg;base64," + b64encode(file_object.getvalue()).decode('ascii')
            # Above Code from https://stackoverflow.com/questions/59581565/how-to-display-flask-image-to-html-directly-without-saving
