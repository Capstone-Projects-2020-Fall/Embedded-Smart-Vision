from multiprocessing.connection import PipeConnection

from ModuleCommunicationHandler.ModuleMessage import ModuleMessage

_Minfo = {
    "version": 1,
    "name": "Web Portal Module",
    "entry_point": -1,
    # The code used to issue messages and establish pipes to the module
    "message_code": "EMM",
}


# Processes any messages left on the queue
def __proc_message__(conn: PipeConnection):
    # if we receive a message on the connection act on it
    if conn.poll():
        m = conn.recv()
        # Verify that the sender used the proper data type to send the message
        if isinstance(m, ModuleMessage):
            # Check if a message code exists for the given module
            ### HANDLE MESSAGES HERE ###
            print("User IO: ", m.message)
        else:
            print("Error! received unknown object as a message!")


# This contains the actual operation of the module which will be run every time
def __operation__():
    ### ADD MODULE OPERATIONS HERE ###
    
    from flask import Blueprint, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email = email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login'))
    
    login_user(user, remember = remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup', methods = ['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email = email).first()
    
    if user:
        flash('Email address already exists')
        return redirect(url_for('main.signup'))
    
    new_user = User(email = email, name = name, password = generate_password_hash(password, method = 'sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('main.login'))

@auth.route('/logout')
def logout():
    return 'Logout'

from flask import Blueprint, render_template
from flask_login import login_required, logout_user, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name = current_user.name)

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.logout'))
    
    # Let the world know we are loading a new object
    img = []
    setup_message = ModuleMessage("WPM",
                                  "ready",
                                  img)
    pass


# Runs the modules functionality
def __load__(conn: PipeConnection):
    
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
    
    # Let the world know we are loading a new object
    setup_message = ModuleMessage("HIO",
                                  "loading",
                                  "Loading " + _Minfo["name"] + "...")
    conn.send(setup_message)

    # Let the world know we are loading a new object
    setup_message = ModuleMessage("HIO",
                                  "ready",
                                  _Minfo["name"] + " done loading!")
    conn.send(setup_message)
    running = True
    # While we are running do operations
    while running:
        __operation__()
        __proc_message__(conn)


# Set the entry point function
_Minfo["entry_point"] = __load__


# Returns a dictionary containing information that describes the module
def __module_info__():
    return _Minfo
