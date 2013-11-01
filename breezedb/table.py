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
.. module:: table
    :platform: Unix, Windows
    :synopsis: Table related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import xml.etree.ElementTree as XML
import os, shutil
from breezedb.breeze_exceptions import BreezeException

def table_exists(table_name, database):
    """ Check whether a table exists in the database or not.
    
        :param table_name: name of the table to check
        :type table_name: str
        :param database: path to the database in which to check
        :type database: str

        :returns: True or False
    """
    breeze_file = os.path.join(database, 'root.breeze')
    breeze_tree = XML.parse(breeze_file)
    breeze_root = breeze_tree.getroot()   
 
    exists = False
    for table in breeze_root:
        if table.text == table_name:
            exists = True
            break

    if not exists:
        return False

    table_path = os.path.join(database, table_name)
    if os.path.exists(table_path):
        exists = True
    else:
        exists  = False

    if not exists:
        return False

    table_file = os.path.join(table_path, 'tableinfo.breeze')
    if os.path.isfile(table_file):
        return True
    else:
        return False

def create_table(table_name, database):
    """ Create a new table in the database.

        Adds a new <table> element to the root.breeze file and create the
        corresponding table structure.

        :param str table_name: name of the new table
        :param str database: path to the database

        :raises BreezeException: database is not writable,
            table already exists, table cannot be created
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('table', 'cannot write to database')

    if table_exists(table_name, database):
        raise BreezeException('table', 'table already exists')

    try:
        newdir = os.path.join(database, table_name)
        os.makedirs(newdir, 0755)

        table_file = os.path.join(newdir, 'tableinfo.breeze')
        breeze_tag = XML.Element('breeze')
        table_tree = XML.ElementTree(breeze_tag)
        table_tree.write(table_file)

        breeze_file = os.path.join(database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        new_table = XML.Element('table')
        new_table.text = table_name
        breeze_root.append(new_table)

        breeze_tree.write(breeze_file)

    except OSError:
        raise BreezeException('table', 'could not create base directory')

    except IOError:
        raise BreezeException('table', 'error writing to file')

def rename_table(table_name, database, new_name):
    """ Rename a table from the database.

        :param str table_name: current name of the table
        :param str database: path to the database
        :param str new_name: new name for the table

        :raises BreezeException: database is not writable,
            the specified table does not exist,
            a table named `new_name` already exists
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('table', 'cannot write to database')

    if not table_exists(table_name, database):
        raise BreezeException('table', 'table does not exist')

    if table_exists(new_name, database):
        raise BreezeException('table', 'table %s already exists'
            % new_name)

    try:
        breeze_file = os.path.join(database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        for table in breeze_root:
            if table.text == table_name:
                table.text = new_name
                break

        breeze_tree.write(breeze_file)

        src = os.path.join(database, table_name)
        dst = os.path.join(database, new_name)
        os.rename(src, dst)

    except IOError:
        raise BreezeException('table', 'could not rename table')

    except OSError:
        raise BreezeException('table', 'cold not rename directory')

def remove_table(table_name, database):
    """ Remove a table from the database.

        Removes the corresponding directory and <table> element
        from root.breeze file

        :param str table_name: name of the table to remove
        :param str database: path to the database

        :raises BreezeException: database is not writable,
            table does not exist
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('table', 'cannot write to database')

    if not table_exists(table_name, database):
        raise BreezeException('table', 'table does not exist')

    try:
        breeze_file = os.path.join(database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        for table in breeze_root:
            if table.text == table_name:
                breeze_root.remove(table)
                break

        breeze_tree.write(breeze_file)

        table_dir = os.path.join(database, table_name)
        shutil.rmtree(table_dir)

    except OSError:
        raise BreezeException('table', 'could not remove table directory')

    except IOError:
        raise BreezeException('table', 'error writing to file')

def get_field_list(table_name, database):
    """ Get a list of fields present in the table.

        :param str table_name: name of the table from which to get
            the fields
        :param str database: path to the database

        :raises BreezeException: table does not exist
    """
    if not table_exists(table_name, database):
        raise BreezeException('table', 'table does not exist')

    fieldlist = []

    table_file = os.path.join(database, table_name, 'tableinfo.breeze')
    table_tree = XML.parse(table_file)
    table_root = table_tree.getroot()

    for field in table_root:
        fieldlist.append(field.text)

    return fieldlist

