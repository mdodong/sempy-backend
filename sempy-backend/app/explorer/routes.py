import sys, os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for

import app.api as api

mod = Blueprint('explorer', __name__)

@mod.route('/')
def homepage():
    latestBlocks = api.get_blocks(15)
    return render_template('explorer.html', latestBlocks=latestBlocks)

@mod.route('/explorer')
def explorer():
    return homepage()

@mod.route('/search', methods=['GET'])
def search():
    query = request.args.get("query")
    if query.isdigit():
        url = url_for('explorer.block_by_number', number=query)
    elif len(query)==42:
        url = url_for('explorer.semux_address', address=query)
    elif len(query) == 66:
        if api.get_block_by_hash(query)["result"] is None:
            url = url_for('explorer.semux_transaction', hash=query)
        else:
            url = url_for('explorer.block_by_hash', hash=query)
    else:
        url = url_for('explorer.homepage')
    return redirect(url)

@mod.route('/explorer/block/<int:number>')
def block_by_number(number):
    block = api.process_block(api.get_block_by_number(number))
    return render_template('block.html', block=block)

@mod.route('/explorer/block/<string:hash>')
def block_by_hash(hash):
    block = api.process_block(api.get_block_by_hash(hash))
    return render_template('block.html', block=block)

@mod.route('/delegates')
def delegates():
    delegates = api.process_all_delegates(api.get_delegates()["result"])
    return render_template('delegates.html', delegates=delegates)

@mod.route('/explorer/address/<string:address>')
def semux_address(address):
    address = api.process_address(api.get_account(address)["result"])
    return render_template("address.html", address=address)

@mod.route('/explorer/transaction/<string:hash>')
def semux_transaction(hash):
    transaction = api.process_transactions(api.get_transaction(hash)["result"])
    return render_template("transaction.html", transaction=transaction)
