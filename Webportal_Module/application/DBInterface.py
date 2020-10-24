from . import db


def add_video(path, tags, app):
    video = db.Video(path=path)
    with app.app_context():
        db.session.add(video)
    for tag in tags:
        new_tag = db.Tag(videoid=video.id, classification=tag)
        with app.app_context():
            db.session.add(new_tag)
    with app.app_context():
        db.session.commit()
