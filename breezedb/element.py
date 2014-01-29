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
.. module:: element
    :platform: Unix, Windows
    :synopsis: Element related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import codecs
from table import exists_table
from field import DTYPES, get_field_type
import parser

def create_row(element_list, table_name, db_path):
    """ Creates a row of elements in the given table.

        Loops through the list of fields in the table and adds the
        corresponding element.

        :param element_list: list of elements to add to the table. Elements
            must appear in the order the fields are listed in the table, and
            there must be one element per field in the list, even if they are
            left blank
        :param str table_name: name of the table that will contain the row
        :param str db_path: path to the database

        :rasies IndexError: invalid number of elements
        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises OSError: error writing to database
        :raises TypeError: data type error
        :raises Exception: table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist', table_name)

        db_data = parser.read(db_path)

        if len(element_list) != len(
                db_data[codecs.decode(table_name, 'utf-8')]['fields']):
            raise Exception('Number of elements is not equal to the number of available fields')
        new_row = {}
        for index, f in enumerate(
                db_data[codecs.decode(table_name, 'utf-8')]['fields']):
            if element_list[index] == "":
                new_row[f.keys()[0]] = ""
            elif f.values()[0] == 'str':
                new_row[f.keys()[0]] = codecs.decode(element_list[index], 'utf-8')
            elif f.values()[0] == 'int' or f.values()[0] == 'bool':
                # Boolean values a represented with 0 or 1
                new_row[f.keys()[0]] = int(element_list[index])
            elif f.values()[0] == 'float':
                new_row[f.keys()[0]] = float(element_list[index])

        db_data[codecs.decode(table_name, 'utf-8')]['rows'].append(new_row)

        parser.write(db_path, db_data)

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e
    except OSError as e:
        raise e
    except TypeError as e:
        raise e
    except ValueError as e:
        raise e

def empty_element(index, field_name, table_name, db_path):
    """ Empty the content of a specific element.

        The content is emptied instead of removing the whole element because
        a single element cannot be removed.

        :param int index: index of the element to empty
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises OSError: error writing to database
        :raises TypeError: invalid index type
        :raises Exception: row does not exist
    """
    try:
        if not exists_row(index, table_name, db_path):
            raise Exception('Row %i does not exist' % index)

        db_data = parser.read(db_path)
        db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]\
                [codecs.decode(field_name, 'utf-8')] = ""
        parser.write(db_path, db_data)

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e
    except OSError as e:
        raise e
    except TypeError as e:
        raise e

def exists_row(index, table_name, db_path):
    """ Check if a row with the given index exists in the table.

        :param int index: index of check
        :param str table_name: name of the table
        :param str db_path: path to the database
        :returns: True or false

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises TypeError: invalid index type
        :raises Exception: table does not exist
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_data = parser.read(db_path)

        if index >= 0 and index < len(
                db_data[codecs.decode(table_name, 'utf-8')]['rows']):
            return True
        else:
            return False

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e
    except TypeError as e:
        raise e

def get_element_data(index, field_name, table_name, db_path):
    """ Get the data contained in a specific element.

        :param int element_index: index of the row
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database
        :returns: content of the element

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises TypeError: invalid index type
        :raises Exception: row does not exist
    """
    try:
        if not exists_row(index, table_name, db_path):
            raise Exception('Row %i does not exist' % index)

        db_data = parser.read(db_path)
        return db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]\
                [codecs.decode(field_name, 'utf-8')]

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e
    except TypeError as e:
        raise e

def modify_element(index, field_name, table_name, db_path, new_content):
    """ Modify the content of an element.

        :param int index: index of the element to modify
        :param str field_name: name of the field that contains the element
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database
        :param str new_content: new content to store in the element

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises OSError: error writing to database
        :raises TypeError: invalid index type
        :raises Exception: row does not exist
    """
    try:
        if not exists_row(index, table_name, db_path):
            raise Exception('Row %i does not exist', index)

        db_data = parser.read(db_path)
        f_type = get_field_type(field_name, table_name, db_path)

        if new_content == "":
            db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]\
                    [codecs.decode(field_name, 'utf-8')] = ""
        elif f_type == 'str':
            db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]\
                    [codecs.decode(field_name, 'utf-8')] =\
                    codecs.decode(new_content, 'utf-8')
        elif f_type == 'int' or f_type == 'bool':
            # Boolean values a represented with 0 or 1
            db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]\
                    [codecs.decode(field_name, 'utf-8')] = int(new_content)
        elif f_type == 'float':
            db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]\
                    [codecs.decode(field_name, 'utf-8')] = float(new_content)

        parser.write(db_path, db_data)

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e
    except OSError as e:
        raise e
    except TypeError as e:
        raise e

def remove_row(index, table_name, db_path):
    """ Remove an element row from the specified table.

        :param int element_index: index of the element row to remove
        :param str table_name: name of the table that contains the field
        :param str database: path to the database

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises KeyError: invalid key
        :raises OSError: error writing to database
        :raises TypeError: invalid index type
        :raises Exception: row does not exist
    """
    try:
        if not exists_row(index, table_name, db_path):
            raise Exception('Row %i does not exist' % index)

        db_data = parser.read(db_path)
        del db_data[codecs.decode(table_name, 'utf-8')]['rows'][index]
        parser.write(db_path, db_data)

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except KeyError as e:
        raise e
    except OSError as e:
        raise e
    except TypeError as e:
        raise e

