# -*- coding: utf-8 -*-
#
# This file is part of breezedb - https://github.com/RMed/breezedb_python
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
.. module:: db
    :platform: Unix, Windows
    :synopsis: DB related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import xml.etree.ElementTree as XML
import os, shutil
from breezedb.breeze_exceptions import BreezeException

def get_table_list(database):
    """ Get a list of tables present in the database's root.breeze file.

        :param str database: path to the database

        :returns: list of all the tables

        :raises BreezeException: directory is not a database
    """
    breeze_file = os.path.join(database, 'root.breeze')
    is_breezedb = os.path.isfile(breeze_file)

    if not is_breezedb:
        raise BreezeException('db', 'not a database')

    tablelist = []

    breeze_file = os.path.join(database, 'root.breeze')
    breeze_tree = XML.parse(breeze_file)
    breeze_root = breeze_tree.getroot()

    for table in breeze_root:
        tablelist.append(table.text)

    return tablelist
        
def create_db(path, name):
    """ Create a database structure in the specified path.

        :param str path: path where the database should be created
        :param str name: name for the database

        :raises BreezeException: cannot write to path,
            cannot create directory, cannot create root.breeze file
    """
    can_write = os.access(path, os.W_OK)
    if not can_write:
        raise BreezeException('db', 'cannot write to path')

    try:
        newdir = os.path.join(path, name)
        os.makedirs(newdir)

        breeze_file = os.path.join(path, name, 'root.breeze')
        breeze_tag = XML.Element('breeze')
        breeze_tree = XML.ElementTree(breeze_tag)
        breeze_tree.write(breeze_file)

    except OSError:
        raise BreezeException('db', 'could not create base directory')

    except IOError:
        raise BreezeException('db', 'error creating the root.breeze file')

def remove_db(path):
    """ Remove the breeze directory structure of the specified path.

        :param str path: Path to the database

        :raises BreezeException: cannot write to path,
            cannot remove the directory
    """
    can_write = os.access(path, os.W_OK)
    breeze_file = os.path.join(path, 'root.breeze')
    is_breezedb = os.path.isfile(breeze_file)

    if not can_write or not is_breezedb:
        raise BreezeException('db', 'cannot remove')

    try:
        shutil.rmtree(path)

    except:
        raise BreezeException('db', 'could not remove the database')

