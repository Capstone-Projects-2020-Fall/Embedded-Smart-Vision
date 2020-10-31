from . import db, video_directory
from .models import Video, Tag
import os


def add_video(path, tags):
    new_path = move_video(path)
    video = Video(path=new_path)
    db.session.add(video)
    db.session.commit()
    for tag in tags:
        new_tag = Tag(videoID=video.id, classification=tag)
        db.session.add(new_tag)
    db.session.commit()
    print("Added Video to database")
    return video.id


def add_tags(videoid, tags):
    for tag in tags:
        new_tag = Tag(videoID=videoid, classification=tag)
        db.session.add(new_tag)
    db.session.commit()
    print("Added Tags to database")


def move_video(path):
    videos = Video.query.all()
    total_videos = len(videos)
    new_video_number = total_videos + 1
    new_name = 'video%d.mp4' % new_video_number
    old_path = os.path.join(os.getcwd(), 'Videos', path)
    new_path = os.path.join(video_directory, new_name)
    os.rename(old_path, new_path)
    return new_name
