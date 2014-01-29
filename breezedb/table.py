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
.. module:: table
    :platform: Unix, Windows
    :synopsis: Table related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import codecs
import db, parser

def create_table(table_name, db_path):
    """ Create a new table in the database.

        :param str table_name: name of the new table
        :param str db_path: path to the database

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: table already exists
    """
    try:
        if exists_table(table_name, db_path):
            raise Exception('Table %s already exists' % table_name)

        db_data = parser.read(db_path)
        db_data[codecs.decode(table_name, 'utf-8')] = {"fields":[],"rows":[]}
        parser.write(db_path, db_data)

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def exists_table(table_name, db_path):
    """ Check whether a table exists in the database or not.
    
        :param str table_name: name of the table to find
        :param str db_path: path to the database
        :returns: True or False

        :raises IOError: cannot open file
        :raises Exception: not a breezedb database
    """
    try:
        if not db.is_brdb(db_path):
            raise Exception('Not a breezedb database: %s' % db_path)

        db_data = parser.read(db_path)
        if table_name.decode('utf-8') in sorted(db_data.iterkeys()):
            return True
        else:
            return False

    except IOError as e:
        raise e

def get_field_list(table_name, db_path):
    """ Get a list of fields present in the table.

        :param str table_name: name of the table
        :param str db_path: path to the database
        :returns: list containing the fields of the table

        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises Exception: table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_data = parser.read(db_path)
        return db_data[codecs.decode(table_name, 'utf-8')]['fields']

    except IOError as e:
        raise e
    except KeyError as e:
        raise e

def get_row(index, table_name, db_path):
    """ Get the elements located in a row of the table.

        :param int index: index of the row
        :param str table_name: name of the table
        :param str db_path: path to the database
        :returns: list containing the data of the row, ordered by field

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises KeyError: invalid field key
        :raises Exception: table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_data = parser.read(db_path)

        elementlist = []
        table = codecs.decode(table_name, 'utf-8')
        for f in db_data[table]['fields']:
            elementlist.append(db_data[table]['rows'][index][f.keys()[0]])

        return elementlist

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e

def get_row_list(table_name, db_path):
    """ Get a list of all the rows in the table

        :param str table_name: name of the table
        :param str db_path: path to the database
        :returns: list of data rows in dictionary format

        :raises IOError: cannot open file
        :raises KeyError: invalid field key
        :raises Exception: table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_data = parser.read(db_path)

        elementlist = []
        table = codecs.decode(table_name, 'utf-8')
        for row in db_data[table]['rows']:
            elementlist.append(row)

        return elementlist

    except IOError as e:
        raise e
    except KeyError as e:
        raise e

def rename_table(table_name, db_path, new_name):
    """ Rename a table from the database.

        :param str table_name: current name of the table
        :param str db_path: path to the database
        :param str new_name: new name for the table

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: table does not exist, new table already exists
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)
        elif exists_table(new_name, db_path):
            raise Exception('Table %s already exists' % new_name)

        db_data = parser.read(db_path)
        db_data[codecs.decode(new_name, 'utf-8')] =\
                db_data[codecs.decode(table_name, 'utf-8')]
        del db_data[codecs.decode(table_name, 'utf-8')]
        parser.write(db_path, db_data)

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def remove_table(table_name, db_path):
    """ Remove a table from the database.

        :param str table_name: name of the table to remove
        :param str db_path: path to the database

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: not a breezedb database, table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_data = parser.read(db_path)
        del db_data[codecs.decode(table_name, 'utf-8')]
        parser.write(db_path, db_data)

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def search_data(data, table_name, db_path, field_name=None, ignore_case=True):
    """ Search data in the table and obtain the index of the rows that
        match the criteria.

        :param str data: data to find
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database
        :param str field_name: name of the field that contains the element.
            If None is specified, then the function will search in all the
            fields of the table in every row
        :param Boolean ignore_case: whether or not to ignore the case
            when searching
        :returns: list of indexes that match the criteria

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: not a breezedb database, table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_data = parser.read(db_path)

        index_list = []
        for index, row in enumerate(db_data[codecs.decode(
                table_name, 'utf-8')]['rows']):
            if field_name:
                element = row[codecs.decode(field_name, 'utf-8')]
                if ignore_case and isinstance(element, (str, unicode)):
                    if data.decode('utf-8').lower() in element.lower():
                        index_list.append(index)
                elif not ignore_case and isinstance(element, (str, unicode)):
                    if data.decode('utf-8') in element:
                        index_list.append(index)
                else:
                    # Numbers
                    if data == element:
                        index_list.append(index)
            else:
                for value in sorted(row.itervalues()):              
                    if ignore_case and isinstance(value, (str, unicode)):
                        if data.decode('utf-8').lower() in value.lower():
                            index_list.append(index)
                            break
                    elif not ignore_case and isinstance(value, (str, unicode)):
                        if data.decode('utf-8') in value:
                            index_list.append(index)
                            break
                    else:
                        # Numbers
                        if data == value:
                            index_list.append(index)
                            break
        return index_list

    except IOError as e:
        raise e
    except OSError as e:
        raise e

