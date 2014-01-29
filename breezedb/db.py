# -*- coding: utf-8 -*-
#
# This file is part of breezedb - https://github.com/RMed/breezedb_python
#
# Copyright (C) 2013-2014  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
# or see <http://www.gnu.org/licenses/>.

"""
.. module:: db
    :platform: Unix, Windows
    :synopsis: DB related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import os
import parser

def create_db(path, name):
    """ Create a database file in the specified path.

        :param str path: path where the database should be created
        :param str name: name for the database

        :raises IOError: cannot write to path
        :raises OSError: error writing to database
        :raises Exception: database already exists
    """
    try:
        db_path = os.path.join(path, name + '.brdb')
        if is_brdb(db_path):
            raise Exception('Database %s already exists' % db_path)

        db_file = open(db_path, 'w')
        db_file.write('{}')
        db_file.close()

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def get_table_list(db_path):
    """ Get a list of tables present in the database.

        :param str db_path: path to the database
        :returns: list of all the tables ordered by key

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: not a breezedb database
    """
    try:
        if not is_brdb(db_path):
            raise Exception('Not a breezedb database: %s' % db_path)

        db_data = parser.read(db_path)

        return sorted(db_data.iterkeys())

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def is_brdb(db_path):
    """ Determine whether the specified file is a breezedb database or not.

        :param str db_path: path to the database
        :returns: True or False
    """
    if os.path.isfile(db_path) and db_path.endswith('.brdb'):
        return True
    else:
        return False

def remove_db(db_path):
    """ Remove the breezedb database in the specified path.

        :param str db_path: path to the database

        :raises IOError: cannot open file
        :raises OSError: cannot delete file
        :raises Exception: not a breezedb database
    """
    try:
        if not is_brdb(db_path):
            raise Exception('Not a breezedb database: %s' % db_path)

        os.remove(db_path)

    except IOError as e:
        raise e
    except OSError as e:
        raise e

