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

from functools import wraps
from flask import request, jsonify
import datetime
from helpers.db import DB
from helpers.utils import Config
import jwt
import os

DEFAULT_EXPIRY_DAYS = 7

# secret key for signing
auth_key = os.environ.get('SECRET_KEY', Config().get('secret_key'))

def token_required(f):
    '''Wrapper for routes that require authentication.

    Args:
        f (func): Function to decorate.

    Returns:
        func: f(user, *args, **kwargs), authenticated as user.
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        # get auth token from request headers
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        
        # if missing, send message and code 401
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        # attempt to decode credentials
        try:
            # get user from token and execute wrapped function as user
            data = jwt.decode(token, auth_key, algorithms=["HS256"])            
            current_user = DB().get_user_info(data['username'])
            if current_user:
                return f(current_user, *args, **kwargs)
        
        # failed to decode credentials
        except Exception as e:
            print(e)

        # invalid token
        return jsonify({'message': 'Token is invalid!'}), 401


    return decorated

def generate_token(username, password):
    '''Given a username and a password, validate credentials and generate an
    auth token.

    Args:
        username (str): Username.
        password (str): Password.
    '''
    user = DB().get_user_info(username) 
    expiry = Config().get('token_expiry_days', DEFAULT_EXPIRY_DAYS)

    if user and user['password'] == password:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=expiry)
        }, auth_key, algorithm="HS256")
        
        return jsonify({'token': token})

    return jsonify({'message': 'invalid credentials'}), 401
