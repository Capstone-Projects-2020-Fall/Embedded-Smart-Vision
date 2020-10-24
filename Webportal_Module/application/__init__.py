from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    from .views.main_page import main_page
    from .views.dashboard import dashboard
    app.register_blueprint(main_page)
    app.register_blueprint(dashboard)

    return app
