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
from flask_cors import CORS
from helpers.db import DB, DBError
from helpers.utils import Config, Logger
from helpers import auth
from helpers import utils

app = Flask(__name__)
CORS(app, supports_credentials=True)

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
        paste_id = DB().add_paste(paste_data)
        Logger().info(f'User {user['username']} uploaded paste {paste_id}.')
        return paste_id
    except DBError as e:
        Logger().error(e)
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
        paste = DB().retrieve_paste(paste_id)
        Logger().info(f'Retrieved paste {paste_id}.')
        return paste
    
    except DBError as e:
        Logger().error(e)
        return jsonify({'message': 'No such paste.'}), 404

@app.route('/list', methods=['GET'])
def list_pastes():
    '''List all pastes.

    Returns:
        list: List of pastes as dicts, with contents omitted.
    '''
    try:
        pastes = DB().get_pastes()
        return pastes
    
    except DBError as e:
        Logger().error(e)
        return None

@app.route('/login', methods=['POST'])
def login():
    '''Log in.

    Returns:
        str: Auth token if successful.
    '''
    token = None
    username = None

    try:
        # pull header from request with username and password
        data = request.get_json()
        username = data['username']
        password = data['password']
        # attempt to generate an auth token
        token = auth.generate_token(username, password)

    except (TypeError, KeyError, DBError):
        return jsonify({'message': 'Authentication failed.'}), 401

    # success
    Logger().info(f'User {username} has logged in successfully.')
    return token

@app.route('/register', methods=['POST'])
def register():
    '''Register a new user.
    '''
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
    except (TypeError, KeyError):
        return jsonify({'message': 'Missing credentials.'}), 400

    # look up list of users
    try:
        users = DB().list_users()
    except DBError as e:
        Logger().error(e)
        return jsonify({'message', 'Internal error.'}), 500

    # make sure username is unique
    if username in users:
        return jsonify({'message': 'Username is taken.'}), 400

    # add user to database
    try:
        DB().add_user(username, password)
    except DBError as e:
        Logger().error(e)
        return jsonify({'message': 'Failed to add user.'}), 500

    # success
    Logger().info(f'User {username} registered successfully.')
    return jsonify({'message': 'Success!'}), 200

if __name__ == '__main__':
    # launch api
    app.run(host='0.0.0.0', debug=True)
