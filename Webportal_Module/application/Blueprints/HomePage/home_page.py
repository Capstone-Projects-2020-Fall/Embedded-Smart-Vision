# import the necessary packages
from flask import Blueprint, render_template


home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.route('/')
def show_home_page():
    # rendering webpage
    return render_template('home_page.html', current_page='home')
