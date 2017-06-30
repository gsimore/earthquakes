"""
let's make a flask app to present the test.
"""
from flask import Flask
from flask import render_template
from earthquakes import *
app = Flask(__name__)

@app.route('/')
@app.route('/<name>')
def map(name=None):
    return render_template('a-map.html', name=name)
