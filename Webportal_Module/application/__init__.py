from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
video_directory = os.path.abspath(os.path.join(os.pardir, 'Videos'))
video_directory = video_directory + '/'
root_directory = os.path.abspath(os.path.join(os.getcwd(), 'application'))
print(video_directory)


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
