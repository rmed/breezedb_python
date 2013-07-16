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
import operations

class ConnectorException(Exception):
    """Class for exceptions in Connector module."""
    def __init__(self, value):
        print 'Connector exception: ', value

class Connector():
    """Connector class.

    Its purpose is to store the path to the database and call the 
    required functions.

    Attributes:
        database -- database path
    """

    def __init__(self, path):
        """Initialization of the Connector.

        Arguments:
            path -- Absolute path to the database directory
        """

        self.database = path

    def get_tablelist(self):
        """Get a list of tables.

        This function returns a list of tables contained in the database.
        The tables are fetched from the root.breeze file.
        """

        tablelist = []

        # Parse the root.breeze file
        breeze_file = os.path.join(self.database, 'root.breeze')
        breeze_tree = XML.parse(breeze_file)
        breeze_root = breeze_tree.getroot()

        # Get all the tables of the database
        for table in root:
            tablelist.append(table.text)

        # Return the list
        return tablelist
        
def create_breezedb(path, name):
    """Create a database structure in the specified path.

    Arguments:
        path -- Absolute path in which to create the database directory
    """

    # Check for write access in the specified path
    can_write = os.access(path, os.W_OK)

    if not can_write:
        # Raise exception
        raise ConnectorException('cannot write to path')

    # Create the directory and an empty root.breeze file
    try:
        # Create directory
        newdir = os.path.join(path, name)
        os.makedirs(newdir)

        # Create root.breeze file
        breeze_file = os.path.join(path, name, 'root.breeze')
        breeze_tag = XML.Element('breeze')
        breeze_tree = XML.ElementTree(breeze_tag)
        breeze_tree.write(breeze_file)

    except OSError:
        # Raise exception
        raise ConnectorException('could not create base directory')

    except IOError:
        # Raise exception
        raise ConnectorException('error creating the root.breeze file')

def remove_breezedb(path):
    """Remove the breeze directory structure of the specified path.

    Arguments:
        path -- Absolute path to the database directory
    """

    # Check for write access and root.breeze in the specified path
    can_write = os.access(path, os.W_OK)
    breeze_file = os.path.join(path, 'root.breeze')
    is_breezedb = os.path.isfile(breeze_file)

    if not can_write or not is_breezedb:
        # Raise exception
        raise ConnectorException('cannot remove')

    # Remove the directory
    try:
        shutil.rmtree(path)

    except:
        # Raise exception
        raise ConnectorException('could not remove the database')

