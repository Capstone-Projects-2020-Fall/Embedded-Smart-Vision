# Web_Main.py
# import the necessary packages
from flask import Flask, render_template, Response

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0', port='5000', debug=True)
