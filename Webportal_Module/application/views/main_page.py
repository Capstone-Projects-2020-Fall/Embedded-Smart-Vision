# main_page.py
# import the necessary packages
from flask import Blueprint, render_template, abort


main_page = Blueprint('main_page', __name__, template_folder='templates/main_page')


@main_page.route('/')
def index():
    # rendering webpage
    return render_template('main_page.html')
