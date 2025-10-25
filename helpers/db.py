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

import helpers.utils as utils

def add_paste(paste):
    '''Write information to the database.

    Args:
        paste (str): Paste contents.

    Returns:
        str: Paste ID if successful.
    '''
    print(f'Writing {paste} to the database')
    id = utils.generate_id()
    return id

def retrieve_paste(id):
    '''Retrieve a paste from the database.

    Args: 
        id (str): Paste ID.

    Returns:
        dict: Paste contents.
    '''
    return id

def get_user_info(username):
    '''Pull user information from the database.

    Args:
        username (str): Username.

    Returns:
        dict: User information.
    '''
    # Mock user database
    users = {
        'testuser': {
            'username': 'testuser',
            'password': 'testpass'
        }
    }

    return users[username]