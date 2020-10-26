from . import db
from .models import Video, Tag


def add_video(path, tags):
    video = Video(path=path)
    db.session.add(video)
    db.session.commit()
    for tag in tags:
        new_tag = Tag(videoID=video.id, classification=tag)
        db.session.add(new_tag)
    db.session.commit()
    print("Added Video to database")
