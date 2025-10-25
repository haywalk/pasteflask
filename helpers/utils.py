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
    
    # must have title
    if not 'title' in paste or not paste['title']:
        return False
    
    # must have content
    if not 'content' in paste or not paste['content']:
        return False

    # must contain an author
    if not 'author' in paste or not paste['author']:
        return False
    
    # must contain a date
    if not 'date' in paste or not paste['date']:
        return False

    return True

def generate_id():
    '''Generate a unique ID.

    Returns:
        str: Unique paste ID.
    '''
    return hex(int(time.time() * 1000))[2:]
