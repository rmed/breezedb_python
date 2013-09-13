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
import os

class FieldException(Exception):
    """Class for exceptions in Field module."""
    def __init__(self, value):
        print 'Field exception: ', value

def exists(field_name, table_name, database):
    """Check whether a field exists in the table or not.

    Returns True in case the field exits and False in case it does not.

    Arguments:
        field_name -- Name of the field to check
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """    
    # Parse the tableinfo.breeze file
    table_file = os.path.join(database, table_name, 'tableinfo.breeze')
    table_tree = XML.parse(table_file)
    table_root = table_tree.getroot()

    # Check if the field is listed in the file
    field_exists = False
    for field in table_root:
        if field.text == field_name:
            # Field exists
            field_exists = True
            break

    # Does the field exist in the file?
    if not field_exists:
        return False

    # Check if the corresponding field file exists
    field_path = os.path.join(database, table_name, field_name)
    if os.path.isfile(field_path):
        # File exists
        return True
    else:
        # File does not exist
        return False

def get_type(field_name, table_name, database):
    """Get the data type of the field.

    Returns the content of the <type> tag in the field file.

    Arguments:
        field_name -- Name of the field to check
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    # Check that the field exists
    if not exists(field_name, table_name, database):
        # Raise exception
        raise FieldException('field does not exist')

    # Parse the file
    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    # Get the type
    return field_root.find('type').text

def add(field_name, field_type, table_name, database):
    """Add a field to the table.

    Add a new <field> element to the tableinfo.breeze file and create the
    corresponding field structure.

    Arguments:
        field_name -- Name of the field to add
        field_type -- Data type that is going to be stored in the field
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise FieldException('cannot write to database')

    # Check if the field already exists in the database
    if exists(field_name, table_name, database):
        # Raise exception
        raise FieldException('field already exists in the table')

    # Add <field> element to tableinfo.breeze and create field structure
    try:
        # Create file
        field_file = os.path.join(database, table_name, field_name)

        # Root
        breeze_tag = XML.Element('breeze')
        field_tree = XML.ElementTree(breeze_tag)
        field_root = field_tree.getroot()

        # Type
        new_type = XML.Element('type')
        new_type.text = field_type

        # Add type to the root and write to file
        field_root.append(new_type)
        field_tree.write(field_file)

        # Add <field> element to tableinfo.breeze file
        # Parse the file
        table_file = os.path.join(database, table_name, 'tableinfo.breeze')
        table_tree = XML.parse(table_file)
        table_root = table_tree.getroot()

        # Add element to root
        new_field = XML.Element('field')
        new_field.text = field_name
        table_root.append(new_field)

        # Write to file
        table_tree.write(table_file)

    except IOError:
        # Raise exception
        raise FieldException('error writing to file')

def rename(field_name, table_name, database, new_name):
    """Modify the name of a field.

    Renames a given field to a new string

    Arguments:
        field_name -- Name of the field to rename
        table_name -- Name of the table that contains the field
        database -- Database that contains the table
        new_name -- New name for the field
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise FieldException('cannot write to database')

    # Check if the field exists in the database
    if not exists(field_name, table_name, database):
        # Raise exception
        raise FieldException('field does not exist in the table')

    # Check if there is a field with the new name already
    if exists(new_name, table_name, database):
        # Raise exception
        raise FieldException('the field %s already exists', new_name)

    # Rename the field
    try:
        # Parse the file
        # Rename the text in the tableinfo.breeze file
        table_file = os.path.join(database, table_name, 'tableinfo.breeze')
        table_tree = XML.parse(table_file)
        table_root = table_tree.getroot()

        # Find the element
        for field in table_root:
            if field.text == field_name:
                # Rename element
                field.text = new_name
                break

        # Write changes to database
        table_tree.write(table_file)

        # Rename the field file
        src = os.path.join(database, table_name, field_name)
        dst = os.path.join(database, table_name, new_name)
        os.rename(src, dst)

    except IOError:
        # Raise exception
        raise FieldException('could not rename the field')

    except OSError:
        # Raise exception
        raise FieldException('could not rename the file')

def remove(field_name, table_name, database):
    """Remove a field from the table.

    Remove the corresponding file and <field> element from tableinfo.breeze

    Arguments:
        field_name -- Name of the field to remove
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise FieldException('cannot write to database')

    # Check if the field exists in the database
    if not exists(field_name, table_name, database):
        # Raise exception
        raise FieldException('field does not exist in the table')

    # Remove field
    try:
        # Remove <field> element from tableinfo.breeze
        # Parse the file
        table_file = os.path.join(database, table_name, 'tableinfo.breeze')
        table_tree = XML.parse(table_file)
        table_root = table_tree.getroot()

        # Find the element
        for field in table_root:
            if field.text == field_name:
                # Remove element
                table_root.remove(field)
                break

        # Write changes to database
        table_tree.write(table_file)

        # Remove file
        field_file = os.path.join (database, table_name, field_name)
        os.remove(field_file)

    except OSError:
        # Raise exception
        raise FieldException('could not remove file')

def empty(field_name, table_name, database):
    """Empty the contents of a field.

    Remove the all the <element> tags from the file but retain the <type>.

    Arguments:
        field_name -- Name of the field to empty
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    # Check for write access in the database
    can_write = os.access(database, os.W_OK)
    if not can_write:
        # Raise exception
        raise FieldException('cannot write to database')

    # Check if the field exists in the database
    if not exists(field_name, table_name, database):
        # Raise exception
        raise FieldException('field does not exist in the table')

    # Parse the file
    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    # Remove all the <element> tags
    for element in field_root.iter('element'):
        field_root.remove(element)

    # Save to file
    field_tree.write(field_file)

def get_elementlist(field_name, table_name, database):
    """Get a list of elements.

    Returns a list of elements present in the specified field.

    Arguments:
        field_name -- Name of the field to check
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    elemlist = []

    # Check that the field exists in the database
    if not exists(field_name, table_name, database):
        # Raise exception
        raise FieldException('field does not exist in the table')

    # Parse the file
    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    # Get all the elements of the field
    for element in field_root.iter('element'):
        elemlist.append(element.text)

    # Return the list
    return elemlist

