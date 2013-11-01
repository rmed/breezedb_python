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
.. module:: field
    :platform: Unix, Windows
    :synopsis: Field related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import xml.etree.ElementTree as XML
import os
from breezedb.breeze_exceptions import BreezeException

def field_exists(field_name, table_name, database):
    """ Check whether a field exists in the table or not.

        :param str field_name: name of the field to check
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :returns: True or False
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
    """ Get the data type of a field from the <type> tag.

        :param str field_name: name of the field to get the type from
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :returns str: type of the field

        :raises BreezeException: field does not exist
    """
    if not field_exists(field_name, table_name, database):
        raise BreezeException('field', 'field does not exist')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    return field_root.find('type').text

def create_field(field_name, field_type, table_name, database):
    """ Create a new field in the table.

        Add a new <field> element to the tableinfo.breeze file and create the
        corresponding field structure.

        :param str field_name: name for the new field
        :param str field_type: type of the new field
        :param str table_name: name of the table that will contain the field
        :param str database: path to the database

        :raises BreezeException: database is not writable,
            a field `field_name` already exists
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('field', 'cannot write to database')

    if field_exists(field_name, table_name, database):
        raise BreezeException('field', 'field already exists in the table')

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
        raise BreezeException('field', 'error writing to file')

def rename_field(field_name, table_name, database, new_name):
    """ Rename a field.

        :param str field_name: current name of the field
        :param str table_name: name of the table that contains the field
        :param str database: path to the database
        :param str new_name: new name for the field

        :raises BreezeException: database is not writable,
            the field to rename does not exist,
            a field `new_name` already exists
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('field', 'cannot write to database')

    if not field_exists(field_name, table_name, database):
        raise BreezeException('field', 'field does not exist in the table')

    if field_exists(new_name, table_name, database):
        raise BreezeException('field', 'the field %s already exists', new_name)

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
        raise BreezeException('field', 'could not rename the field')

    except OSError:
        raise BreezeException('field', 'could not rename the file')

def remove_field(field_name, table_name, database):
    """ Remove a field from the table.

        Remove the corresponding file and <field> element
        from the tableinfo.breeze file

        :param str field_name: name of the field to remove
        :param str table_name: name of the table that contains the field
        :param str database: path to the database
        
        :raises BreezeException: database is not writable,
            field does not exist
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('field', 'cannot write to database')

    if not field_exists(field_name, table_name, database):
        raise BreezeException('field', 'field does not exist in the table')

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
        raise BreezeException('field', 'could not remove file')

def empty_field(field_name, table_name, database):
    """ Empty the contents of a field.

        Remove the all the <element> tags from the file but
        preserve the <type> tab.

        :param str field_name: name of the field to empty
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :raises BreezeException: database is not writable,
            field does not exist
    """
    can_write = os.access(database, os.W_OK)
    if not can_write:
        raise BreezeException('field', 'cannot write to database')

    if not field_exists(field_name, table_name, database):
        raise BreezeException('field', 'field does not exist in the table')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    for element in field_root.iter('element'):
        field_root.remove(element)

    field_tree.write(field_file)

def get_element_list(field_name, table_name, database):
    """ Get a list of elements contained in the field.

        :param str field_name: name of the field to get the elements from
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :returns: list of elements

        :raises BreezeException: field does not exist
    """
    elemlist = []

    if not field_exists(field_name, table_name, database):
        raise BreezeException('field', 'field does not exist in the table')

    field_file = os.path.join(database, table_name, field_name)
    field_tree = XML.parse(field_file)
    field_root = field_tree.getroot()

    for element in field_root.iter('element'):
        elemlist.append(element.text)

    return elemlist

