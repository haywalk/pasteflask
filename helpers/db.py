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
import sqlite3

DEFAULT_DATABASE = 'pasteflask.db'


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

            # open connection to database
            database_name = Config().get('database_name', DEFAULT_DATABASE)
            cls._instance.connection = sqlite3.connect(database_name)


            # create tables if they don't exist already
            cursor = cls._instance.connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS\
                users(username PRIMARY KEY, password)')
            cursor.execute('CREATE TABLE IF NOT EXISTS\
                pastes(id PRIMARY KEY, title, content, author, date)')
            cursor.close()

        return cls._instance

    def add_paste(self, paste):
        '''Write information to the database.

        Args:
            paste (str): Paste contents.

        Returns:
            str: Paste ID if successful.
        '''
        id = generate_id()
        title = paste['title']
        content = paste['content']    
        author = paste['author']
        date = paste['date']

        # insert into pastes table
        cursor = self.connection.cursor()
        cursor.execute(f'INSERT INTO pastes VALUES\
            ("{id}", "{title}", "{content}", "{author}", "{date}")')
        cursor.close()
        self.connection.commit()

        return id

    def retrieve_paste(self, id):
        '''Retrieve a paste from the database.

        Args: 
            id (str): Paste ID.

        Returns:
            dict: Paste contents.
        '''
        # pull paste from database
        cursor = self.connection.cursor()
        result = cursor.execute(f'SELECT * FROM pastes WHERE id = "{id}"')
        paste_data = result.fetchone()
        cursor.close()

        # format response
        paste = {
            'id': paste_data[0],
            'title': paste_data[1],
            'content': paste_data[2],
            'author': paste_data[3],
            'date': paste_data[4]
        }

        return paste

    def get_user_info(self, username):
        '''Pull user information from the database.

        Args:
            username (str): Username.

        Returns:
            dict: User information.
        '''
        # get user info from database
        cursor = self.connection.cursor()
        result = cursor.execute(f'SELECT * FROM users WHERE username = "{username}"')
        user_data = result.fetchone()
        cursor.close()

        # format response
        user = {
            'username': user_data[0],
            'password': user_data[1]
        }

        return user
    
    def get_pastes(self):
        '''Return a list of pastes in the database.
        '''
        # pull all paste summaries
        cursor = self.connection.cursor()
        result = cursor.execute(f'SELECT id, title, author, date\
            FROM pastes ORDER BY date DESC')
        pastes_raw = result.fetchall()
        cursor.close()

        # format to list
        pastes = []
        for paste in pastes_raw:
            this_paste = {
                'id': paste[0],
                'title': paste[1],
                'author': paste[2],
                'date': paste[3]
            }
            pastes.append(this_paste)

        return pastes