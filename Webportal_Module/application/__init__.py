from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from Webportal_Module.application.VideoStream.VideoFeed import VideoStream

db = SQLAlchemy()
root_directory = os.path.abspath(os.path.join(os.getcwd(), 'Webportal_Module', 'application'))
root_directory = root_directory + '/'

video_directory = os.path.abspath(os.path.join(root_directory, 'static'))
video_directory = video_directory + '/'

video_stream = VideoStream()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    from Webportal_Module.application.Blueprints.HomePage.home_page import home_page
    from Webportal_Module.application.Blueprints.Dashboard.dashboard import dashboard
    from Webportal_Module.application.Blueprints.VideoGallery.video_gallery import video_gallery
    app.register_blueprint(home_page)
    app.register_blueprint(dashboard)
    app.register_blueprint(video_gallery)

    return app
