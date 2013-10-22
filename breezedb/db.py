# -*- coding: utf-8 -*-
#
# This file is part of BreezeDB - https://github.com/RMed/breezedb_python
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

import xml.etree.ElementTree as XML
import shutil, os

class DBException(Exception):
    """Class for exceptions in DB module."""
    def __init__(self, value):
        print 'Database exception: ', value

def get_tablelist(database):
    """Get a list of tables.

    This function returns a list of tables contained in the database.
    The tables are fetched from the root.breeze file.
    """
    tablelist = []

    breeze_file = os.path.join(database, 'root.breeze')
    breeze_tree = XML.parse(breeze_file)
    breeze_root = breeze_tree.getroot()

    for table in breeze_root:
        tablelist.append(table.text)

    return tablelist
        
def create_db(path, name):
    """Create a database structure in the specified path.

    Arguments:
        path -- Absolute path in which to create the database directory
    """
    can_write = os.access(path, os.W_OK)
    if not can_write:
        raise DBException('cannot write to path')

    try:
        newdir = os.path.join(path, name)
        os.makedirs(newdir)

        breeze_file = os.path.join(path, name, 'root.breeze')
        breeze_tag = XML.Element('breeze')
        breeze_tree = XML.ElementTree(breeze_tag)
        breeze_tree.write(breeze_file)

    except OSError:
        raise DBException('could not create base directory')

    except IOError:
        raise DBException('error creating the root.breeze file')

def remove_db(path):
    """Remove the breeze directory structure of the specified path.

    Arguments:
        path -- Absolute path to the database directory
    """
    can_write = os.access(path, os.W_OK)
    breeze_file = os.path.join(path, 'root.breeze')
    is_breezedb = os.path.isfile(breeze_file)

    if not can_write or not is_breezedb:
        raise DBException('cannot remove')

    try:
        shutil.rmtree(path)

    except:
        raise DBException('could not remove the database')

