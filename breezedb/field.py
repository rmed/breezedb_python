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
import os

class FieldException(Exception):
    """Class for exceptions in Field module."""
    def __init__(self, value):
        print 'Field exception: ', value

def field_exists(field_name, table_name, database):
    """Check whether a field exists in the table or not.

    Returns True in case the field exits and False in case it does not.

    Arguments:
        field_name -- Name of the field to check
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """    
    table_file = os.path.join(database, table_name, 'tableinfo.breeze')
    table_tree = XML.parse(table_file)
    table_root = table_tree.getroot()

    exists = False
    for field in table_root:
        if field.text == field_name:
            exists = True
            break

    if not exists:
        return False

    field_path = os.path.join(database, table_name, field_name)
    if os.path.isfile(field_path):
        return True
    else:
        return False

def get_field_type(field_name, table_name, database):
    """Get the data type of the field.

    Returns the content of the <type> tag in the field file.

    Arguments:
        field_name -- Name of the field to check
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    if not field_exists(field_name, table_name, database):
        raise FieldException('field does not exist')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    return field_root.find('type').text

def create_field(field_name, field_type, table_name, database):
    """Add a field to the table.

    Add a new <field> element to the tableinfo.breeze file and create the
    corresponding field structure.

    Arguments:
        field_name -- Name of the field to add
        field_type -- Data type that is going to be stored in the field
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise FieldException('cannot write to database')

    if field_exists(field_name, table_name, database):
        raise FieldException('field already exists in the table')

    try:
        field_file = os.path.join(database, table_name, field_name)

        breeze_tag = XML.Element('breeze')
        field_tree = XML.ElementTree(breeze_tag)
        field_root = field_tree.getroot()

        new_type = XML.Element('type')
        new_type.text = field_type

        field_root.append(new_type)
        field_tree.write(field_file)

        table_file = os.path.join(database, table_name, 'tableinfo.breeze')
        table_tree = XML.parse(table_file)
        table_root = table_tree.getroot()

        new_field = XML.Element('field')
        new_field.text = field_name
        table_root.append(new_field)

        table_tree.write(table_file)

    except IOError:
        raise FieldException('error writing to file')

def rename_field(field_name, table_name, database, new_name):
    """Modify the name of a field.

    Renames a given field to a new string

    Arguments:
        field_name -- Name of the field to rename
        table_name -- Name of the table that contains the field
        database -- Database that contains the table
        new_name -- New name for the field
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise FieldException('cannot write to database')

    if not field_exists(field_name, table_name, database):
        raise FieldException('field does not exist in the table')

    if field_exists(new_name, table_name, database):
        raise FieldException('the field %s already exists', new_name)

    try:
        table_file = os.path.join(database, table_name, 'tableinfo.breeze')
        table_tree = XML.parse(table_file)
        table_root = table_tree.getroot()

        for field in table_root:
            if field.text == field_name:
                field.text = new_name
                break

        table_tree.write(table_file)

        src = os.path.join(database, table_name, field_name)
        dst = os.path.join(database, table_name, new_name)
        os.rename(src, dst)

    except IOError:
        raise FieldException('could not rename the field')

    except OSError:
        raise FieldException('could not rename the file')

def remove_field(field_name, table_name, database):
    """Remove a field from the table.

    Remove the corresponding file and <field> element from tableinfo.breeze

    Arguments:
        field_name -- Name of the field to remove
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise FieldException('cannot write to database')

    if not field_exists(field_name, table_name, database):
        raise FieldException('field does not exist in the table')

    try:
        table_file = os.path.join(database, table_name, 'tableinfo.breeze')
        table_tree = XML.parse(table_file)
        table_root = table_tree.getroot()

        for field in table_root:
            if field.text == field_name:
                table_root.remove(field)
                break

        table_tree.write(table_file)

        field_file = os.path.join (database, table_name, field_name)
        os.remove(field_file)

    except OSError:
        raise FieldException('could not remove file')

def empty_field(field_name, table_name, database):
    """Empty the contents of a field.

    Remove the all the <element> tags from the file but retain the <type>.

    Arguments:
        field_name -- Name of the field to empty
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise FieldException('cannot write to database')

    if not field_exists(field_name, table_name, database):
        raise FieldException('field does not exist in the table')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    for element in field_root.iter('element'):
        field_root.remove(element)

    field_tree.write(field_file)

def get_element_list(field_name, table_name, database):
    """Get a list of elements.

    Returns a list of elements present in the specified field.

    Arguments:
        field_name -- Name of the field to check
        table_name -- Name of the table that contains the field
        database -- Database to check (usually obtained from the Connector)
    """
    elemlist = []

    if not field_exists(field_name, table_name, database):
        raise FieldException('field does not exist in the table')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    for element in field_root.iter('element'):
        elemlist.append(element.text)

    return elemlist

