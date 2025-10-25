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

from helpers.utils import Config, generate_id

class DB:
    '''Singleton database for storing user information and pastes.
    '''
    _instance = None

    def __new__(cls):
        '''Retrieve the instance of the database or create a new one if it
        doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
            # mock user db
            cls._instance.users = {
                'testuser': {
                    'username': 'testuser',
                    'password': 'testpass'
                }
            }

            # mock paste db
            cls._instance.pastes = {}
        
        return cls._instance

    def add_paste(self, paste):
        '''Write information to the database.

        Args:
            paste (str): Paste contents.

        Returns:
            str: Paste ID if successful.
        '''
        id = generate_id()
        self.pastes[id] = paste
        print(self.pastes)
        return id

    def retrieve_paste(self, id):
        '''Retrieve a paste from the database.

        Args: 
            id (str): Paste ID.

        Returns:
            dict: Paste contents.
        '''
        return self.pastes[id]

    def get_user_info(self, username):
        '''Pull user information from the database.

        Args:
            username (str): Username.

        Returns:
            dict: User information.
        '''
        return self.users[username]