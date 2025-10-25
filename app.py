#!/usr/bin/env python3

# Copyright 2025 Hayden Walker. 
#
# This file is part of Pasteflask.
# 
# Pasteflask is free software: you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Pasteflask is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with
# Pasteflask. If not, see <https://www.gnu.org/licenses/>. 

from flask import Flask, request, jsonify
import helpers.db as db
import helpers.auth as auth
import helpers.utils as utils
import time

app = Flask(__name__)

@app.route('/paste', methods=['POST'])
@auth.token_required
def paste(user):
    '''Upload a paste.
    '''
    # get paste data from request
    paste = request.get_json()

    # add metadata
    paste['author'] = user['username']
    paste['date'] = int(time.time() * 1000)

    # validate paste
    if not utils.validate_paste(paste):
        return jsonify({'message', 'Malformed paste.'}), 400

    # put in database
    try:
        return db.add_paste(paste)
    except:
        return jsonify({'message': 'Failed to paste.'}), 500

@app.route('/retrieve/<id>', methods=['GET'])
def retrieve(id):
    '''Retrieve a paste.

    Args:
        id (str): ID of paste to retrieve.

    Returns:
        str: Contents of paste.
    '''
    try:
        return db.retrieve_paste(id)
    except:
        return jsonify({'message': 'No such paste.'}), 404

@app.route('/login', methods=['POST'])
def login():
    '''Log in.

    Returns:
        str: Auth token if successful.
    '''
    # pull header from request with username and password
    data = request.get_json()    
    if not data or not data['username'] or not data['password']:
        return jsonify({'message': 'Missing credentials.'}), 400

    # attempt to generate an auth token
    return auth.generate_token(data['username'], data['password'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    