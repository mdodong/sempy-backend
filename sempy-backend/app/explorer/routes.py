import sys, os
from flask import Blueprint, jsonify, render_template

import app.api as api

mod = Blueprint('explorer', __name__)

@mod.route('/')
def homepage():
    latestBlocks = api.get_blocks(20)
    return render_template('explorer.html', latestBlocks=latestBlocks)

@mod.route('/explorer')
def explorer():
    return homepage()
