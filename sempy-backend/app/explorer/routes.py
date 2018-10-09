import sys, os
from flask import Blueprint, jsonify, render_template
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import app.api

mod = Blueprint('explorer', __name__)

@mod.route('/')
def home():
    #return jsonify(api.get_delegates()) #
    #return '<h1>This is the Homepage</h1>'
    return render_template('index.html')
