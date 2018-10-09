import sys, os
from flask import Blueprint, jsonify, render_template

import app.api

mod = Blueprint('explorer', __name__)

@mod.route('/')
def homepage():
    #return jsonify(api.get_delegates()) #
    #return '<h1>This is the Homepage</h1>'
    return render_template('explorer.html')
