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

import time
from flask import Flask, request, jsonify
from helpers.db import DB
from helpers.utils import Config
from helpers import auth
from helpers import utils

app = Flask(__name__)

@app.route('/paste', methods=['POST'])
@auth.token_required
def paste(user):
    '''Upload a paste.
    '''
    # get paste data from request
    paste_data = request.get_json()

    # add metadata
    paste_data['author'] = user['username']
    paste_data['date'] = int(time.time() * 1000)

    # validate paste
    if not utils.validate_paste(paste_data):
        return jsonify({'message', 'Malformed paste.'}), 400

    # put in database
    try:
        return DB().add_paste(paste_data)
    except Exception as e:
        print('pastefail')
        print(e)
        return jsonify({'message': 'Failed to paste.'}), 500

@app.route('/retrieve/<paste_id>', methods=['GET'])
def retrieve(paste_id):
    '''Retrieve a paste.

    Args:
        id (str): ID of paste to retrieve.

    Returns:
        str: Contents of paste.
    '''
    try:
        return DB().retrieve_paste(paste_id)
    except Exception as e:
        print(e)
        return jsonify({'message': 'No such paste.'}), 404

@app.route('/list', methods=['GET'])
def list_pastes():
    '''List all pastes.

    Returns:
        list: List of pastes as dicts, with contents omitted.
    '''
    pastes = DB().get_pastes()
    return pastes

@app.route('/login', methods=['POST'])
def login():
    '''Log in.

    Returns:
        str: Auth token if successful.
    '''
    try:
        # pull header from request with username and password
        data = request.get_json()

        # attempt to generate an auth token
        return auth.generate_token(data['username'], data['password'])

    except:
        return jsonify({'message': 'Authentication failed.'}), 401

@app.route('/register', methods=['POST'])
def register():
    '''Register a new user.
    '''

    print('asdf')
    username = None
    password = None
    users = None

    # make sure registration is enabled
    registration_enabled = Config().get('registration_enabled', False)
    if not registration_enabled:
        return jsonify({'message': 'Registration disabled.'}), 403

    # get information from request
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
    except:
        return jsonify({'message': 'Missing credentials.'}), 400

    # look up list of users
    try:
        users = DB().list_users()
    except:
        return jsonify({'message', 'Internal error.'}), 500

    # make sure username is unique
    if username in users:
        return jsonify({'message': 'Username is taken.'}), 400

    # add user to database
    try:
        DB().add_user(username, password)
    except:
        return jsonify({'message': 'Failed to add user.'}), 500

    # success
    return jsonify({'message': 'Success!'}), 200

if __name__ == '__main__':
    # launch api
    app.run(host='0.0.0.0', debug=True)
