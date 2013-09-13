# -*- coding: utf-8 -*-
# This file is part of BreezeDB - https://github.com/RMed/breeze_db
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import xml.etree.ElementTree as XML
import os, shutil

class TableException(Exception):
    """Class for exceptions in Table module."""
    def __init__(self, value):
        print 'Table exception: ', value

def exists(table_name, database):
    """Check whether a table exists in the database or not.

    Returns True in case the table exits and False in case it does not.

    Arguments:
        table_name -- Name of the table to check
        database -- Database to check (usually obtained from the Connector)
    """
    # Check the root.breeze file for the table
    breeze_file = os.path.join(database, 'root.breeze')
    breeze_tree = XML.parse(breeze_file)
    breeze_root = breeze_tree.getroot()   
 
    # Check if the table is listed
    table_exists = False
    for table in breeze_root:
        if table.text == table_name:
            # Table exists in the file
            table_exists = True
            break

    # Does the table exist in the file?
    if not table_exists:
        return False

    # Check if the directory corresponding to the table exists
    table_path = os.path.join(database, table_name)
    if os.path.exists(table_path):
        # Directory exists
        table_exists = True
    else:
        # Directory does not exist
        table_exists  = False

    # Does the directory exist?
    if not table_exists:
        return False

    # Check if the tableinfo.breeze file exists
    table_file = os.path.join(table_path, 'tableinfo.breeze')
    if os.path.isfile(table_file):
        # File exists
        return True
    else:
        # File does not exist
        return False

def add(table_name, database):
    """Add a table to the database.

    Add a new <table> element to the root.breeze file and create the
    corresponding table structure.

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise TableException('cannot write to database')

    # Check if the table already exists in the database
    if exists(table_name, database):
        # Raise exception
        raise TableException('table already exists in the database')

    # Add <table> element to root.breeze and create table structure
    try:
        # Create directory
        newdir = os.path.join(database, table_name)
        os.makedirs(newdir, 0755)

        # Create tableinfo.breeze file
        table_file = os.path.join(newdir, 'tableinfo.breeze')
        breeze_tag = XML.Element('breeze')
        table_tree = XML.ElementTree(breeze_tag)
        table_tree.write(table_file)

        # Add <table> element to root.breeze
        # Parse the file
        breeze_file = os.path.join(database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        # Add element to root
        new_table = XML.Element('table')
        new_table.text = table_name
        breeze_root.append(new_table)

        # Write to file
        breeze_tree.write(breeze_file)

    except OSError:
        # Raise exception
        raise TableException('could not create base directory')

    except IOError:
        # Raise exception
        raise TableException('error writing to file')

def rename(table_name, database, new_name):
    """Rename a table from the database.

    Renames a given table to a new string

    Arguments:
        table_name -- Name of the table to rename
        database -- Database that contains the table
        new_name -- New name for the table
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise TableException('cannot write to database')

    # Check that the table exists
    if not exists(table_name, database):
        # Raise exception
        raise TableException('table does not exist')

    # Check if there is a table with the new name already
    if exists(new_name, database):
        # Raise exception
        raise TableException('there table %s already exists', new_name)

    # Rename table
    try:
        # Parse the file
        breeze_file = os.path.join(database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        # Find the element
        for table in breeze_root:
            if table.text == table_name:
                # Remove element
                table.text = new_name
                break

        # Write changes to database
        breeze_tree.write(breeze_file)

        # Rename the directory
        src = os.path.join(database, table_name)
        dst = os.path.join(database, new_name)
        os.rename(src, dst)

    except IOError:
        # Raise exception
        raise TableException('could not rename table')

    except OSError:
        # Raise exception
        raise TableException('cold not rename directory')

def remove(table_name, database):
    """Remove a table from the database.

    Removes the corresponding directory and <table> element from root.breeze

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise TableException('cannot write to database')

    # Check that the table exists
    if not exists(table_name, database):
        # Raise exception
        raise TableException('table does not exist')

    # Remove table
    try:
        # Remove <table> element from root.breeze
        # Parse the file
        breeze_file = os.path.join(database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        # Find the element
        for table in breeze_root:
            if table.text == table_name:
                # Remove element
                breeze_root.remove(table)
                break

        # Write changes to database
        breeze_tree.write(breeze_file)

        # Remove the directory
        table_dir = os.path.join(database, table_name)
        shutil.rmtree(table_dir)

    except OSError:
        # Raise exception
        raise TableException('could not remove table directory')

    except IOError:
        # Raise exception
        raise TableException('error writing to file')

def get_fieldlist(table_name, database):
    """Get a list of fields.

    Returns a list of fields present in the specified table.

    Arguments:
        table_name -- Name of the table to create
        database -- Database to check (usually obtained from the Connector)
    """
    fieldlist = []

    # Parse the tableinfo.breeze file
    table_file = os.path.join(database, table_name, 'tableinfo.breeze')
    table_tree = XML.parse(table_file)
    table_root = table_tree.getroot()

    # Get all the fields of the table
    for field in table_root:
        fieldlist.append(field.text)

    # Return the list
    return fieldlist

