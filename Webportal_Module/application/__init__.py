from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from Webportal_Module.application.VideoStream.VideoFeed import VideoStream

db = SQLAlchemy()
video_directory = os.path.abspath(os.path.join(os.getcwd(), 'Videos'))
video_directory = video_directory + '/'
print(video_directory)
root_directory = os.path.abspath(os.path.join(os.getcwd(), 'Webportal_Module', 'application'))
root_directory = root_directory + '/'
print(root_directory)
video_stream = VideoStream()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    from .views.main_page import main_page
    from .views.dashboard import dashboard
    from .views.video_gallery import video_gallery
    app.register_blueprint(main_page)
    app.register_blueprint(dashboard)
    app.register_blueprint(video_gallery)

    return app
