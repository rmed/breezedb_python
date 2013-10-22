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
import os, shutil

class TableException(Exception):
    """Class for exceptions in Table module."""
    def __init__(self, value):
        print 'Table exception: ', value

def table_exists(table_name, database):
    """Check whether a table exists in the database or not.

    Returns True in case the table exits and False in case it does not.

    Arguments:
        table_name -- Name of the table to check
        database -- Database to check (usually obtained from the Connector)
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
    """Add a table to the database.

    Add a new <table> element to the root.breeze file and create the
    corresponding table structure.

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise TableException('cannot write to database')

    if table_exists(table_name, database):
        raise TableException('table already exists in the database')

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
        raise TableException('could not create base directory')

    except IOError:
        raise TableException('error writing to file')

def rename_table(table_name, database, new_name):
    """Rename a table from the database.

    Renames a given table to a new string

    Arguments:
        table_name -- Name of the table to rename
        database -- Database that contains the table
        new_name -- New name for the table
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise TableException('cannot write to database')

    if not table_exists(table_name, database):
        raise TableException('table does not exist')

    if table_exists(new_name, database):
        raise TableException('there table %s already exists', new_name)

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
        raise TableException('could not rename table')

    except OSError:
        raise TableException('cold not rename directory')

def remove_table(table_name, database):
    """Remove a table from the database.

    Removes the corresponding directory and <table> element from root.breeze

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise TableException('cannot write to database')

    if not table_exists(table_name, database):
        raise TableException('table does not exist')

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
        raise TableException('could not remove table directory')

    except IOError:
        raise TableException('error writing to file')

def get_field_list(table_name, database):
    """Get a list of fields.

    Returns a list of fields present in the specified table.

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """
    fieldlist = []

    table_file = os.path.join(database, table_name, 'tableinfo.breeze')
    table_tree = XML.parse(table_file)
    table_root = table_tree.getroot()

    for field in table_root:
        fieldlist.append(field.text)

    return fieldlist

