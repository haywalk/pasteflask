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
import yaml

CONFIG_FILE = './config.yaml'


class Config:
    '''Singleton configuration.
    '''
    _instance = None

    def __new__(cls):
        '''Retrieve the instance of the database or create a new one if it
        doesn't exist.
        '''
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reload(CONFIG_FILE)
        
        return cls._instance

    def reload(self, config_file):
        '''Load a YAML configuration file.

        Args:
            config_file (str): Path to config file.

        Return:
            dict: Configuration.
        '''
        with open(config_file, 'r') as file:
            data = yaml.safe_load(file)
        
        self.config_data = data
    
    def get(self, attribute, default=None):
        '''Get an attribute from the configuration.

        Args:
            attribute (str): Attribute to get.
            default (str): Value to default to if not found (default None)
        '''
        try:
            return self.config_data[attribute]
        except KeyError:
            return default


def validate_paste(paste):
    '''Validate a paste.

    Args:
        paste (dict): Paste to validate.

    Returns: 
        bool: True if valid.
    '''
    # must not be null
    if not paste:
        return False
    
    # all required fields must be present
    for field in Config().get('paste_required_fields', []):
        if field not in paste or not paste[field]:
            return False

    return True

def generate_id():
    '''Generate a unique ID.

    Returns:
        str: Unique paste ID.
    '''
    return hex(int(time.time() * 1000))[2:]
