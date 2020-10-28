from . import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), unique=True, nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    videoID = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    classification = db.Column(db.String(100), nullable=False)
