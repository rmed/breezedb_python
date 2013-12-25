# -*- coding: utf-8 -*-
#
# This file is part of breezedb - https://github.com/RMed/breezedb_python
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
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
.. module:: field
    :platform: Unix, Windows
    :synopsis: Field related operations.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import codecs, json, os
import table

def create_field(field_name, table_name, db_path):
    """ Create a new field in the table.

        Adds the empty field to already existing rows.

        :param str field_name: name for the new field
        :param str table_name: name of the table that will contain the field
        :param str db_path: path to the database

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: field already exists
    """
    try:
        if exists_field(field_name, table_name, db_path):
            raise Exception('Field %s already exists' % field_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        db_data[codecs.decode(table_name, 'utf-8')]['fields'].append(
                codecs.decode(field_name, 'utf-8'))

        for row in db_data[codecs.decode(table_name, 'utf-8')]['rows']:
            row[codecs.decode(field_name, 'utf-8')] = ""

        db_file = codecs.open(db_path, 'w', 'utf-8')
        db_file.write(json.dumps(db_data, ensure_ascii=False,
                sort_keys=True, indent=4))
        db_file.close()

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def empty_field_row(index, field_name, table_name, db_path):
    """ Empty the contents of a field on a single row of the table.

        :param int index: index of the desired row
        :param str field_name: name of the field to empty
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: field does not exist
    """
    try:
        if not exists_field(field_name, table_name, db_path):
            raise Exception('Field %s does not exist' % field_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        db_data[codecs.decode(table_name, 'utf-8')]['rows']\
                [index][codecs.decode(field_name, 'utf-8')] = ""

        db_file = codecs.open(db_path, 'w', 'utf-8')
        db_file.write(json.dumps(db_data, ensure_ascii=False,
                sort_keys=True, indent=4))
        db_file.close()

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except OSError as e:
        raise e

def empty_field_table(field_name, table_name, db_path):
    """ Empty the contents of a field on every row of the table.

        :param str field_name: name of the field to empty
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: field does not exist
    """
    try:
        if not exists_field(field_name, table_name, db_path):
            raise Exception('Field %s does not exist' % field_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        for row in db_data[codecs.decode(table_name, 'utf-8')]['rows']:
            row[codecs.decode(field_name, 'utf-8')] = ""

        db_file = codecs.open(db_path, 'w', 'utf-8')
        db_file.write(json.dumps(db_data, ensure_ascii=False,
                sort_keys=True, indent=4))
        db_file.close()

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def exists_field(field_name, table_name, db_path):
    """ Check whether a field exists in the table or not.

        :param str field_name: name of the field to check
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database
        :returns: True or False

        :raises IOError: cannot open file
    """    
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        if field_name.decode('utf-8') in \
                db_data[codecs.decode(table_name, 'utf-8')]['fields']:
            return True
        else:
            return False

    except IOError as e:
        raise e

def get_field_data(field_name, table_name, db_path):
    """ Get the data contained in the field for every row in the table.

        :param str field_name: name of the field to get the elements from
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database

        :returns: data list sorted by order of appearance

        :raises IOError: cannot open file
        :raises KeyError: invalid field key
        :raises Exception: field does not exist
    """
    try:
        if not exists_field(field_name, table_name, db_path):
            raise Exception('Field %s does not exist' % field_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        datalist = []
        for row in db_data[codecs.decode(table_name, 'utf-8')]['rows']:
            datalist.append(row[codecs.decode(field_name, 'utf-8')])

        return datalist

    except IOError as e:
        raise e
    except KeyError as e:
        raise e

def rename_field(field_name, table_name, db_path, new_name):
    """ Rename a field.

        Renames both the element in the `fields` list and every row of
        the table.

        :param str field_name: current name of the field
        :param str table_name: name of the table that contains the field
        :param str db_path: path to the database
        :param str new_name: new name for the field

        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: field does not exist, new field already exists
    """
    try:
        if not exists_field(table_name, db_path):
            raise Exception('Field %s does not exist'% field_name)
        elif exists_field(new_name, db_path):
            raise Exception('Field %s already exists' % new_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        for index, field in enumerate(
                db_data[codecs.decode(table_name, 'utf-8')]['fields']):
            if field_name.decode('utf-8') == field:
                db_data[codecs.decode(table_name, 'utf-8')]['fields'][index] =\
                         codecs.decode(new_name, 'utf-8')
                break

        for row in db_data[codecs.decode(table_name, 'utf-8')]['rows']:
            row[codecs.decode(new_name, 'utf-8')] =\
                    row[codecs.decode(field_name, 'utf-8')]
            del row[codecs.decode(field_name, 'utf-8')]

        db_file = codecs.open(db_path, 'w', 'utf-8')
        db_file.write(json.dumps(db_data, ensure_ascii=False,
                sort_keys=True, indent=4))
        db_file.close()

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def remove_field(field_name, table_name, db_path):
    """ Remove a field from the table.

        Removes the field from both the list of fields and every row of
        the table.

        :param str field_name: name of the field to remove
        :param str table_name: name of the table that contains the field
        :param str database: path to the database
        
        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises Exception: field does not exist
    """
    try:
        if not exists_field(table_name, db_path):
            raise Exception('Field %s does not exist' % field_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        for index, field in enumerate(
                db_data[codecs.decode(table_name, 'utf-8')]['fields']):
            if field_name.decode('utf-8') == field:
                del db_data[codecs.decode(table_name, 'utf-8')]['fields'][index]
                break

        for row in db_data[codecs.decode(table_name, 'utf-8')]['rows']:
            del row[codecs.decode(field_name, 'utf-8')]

        db_file = codecs.open(db_path, 'w', 'utf-8')
        db_file.write(json.dumps(db_data, ensure_ascii=False,
                sort_keys=True, indent=4))
        db_file.close()

    except IOError as e:
        raise e
    except OSError as e:
        raise e

def swap_fields(index1, index2, table_name, db_path):
    """ Swap two field indexes in the specified table. This affects the
        priority order of the fields.

        :param int index1: first field index to swap
        :param int index2: second field index to swap
        :param str table_name: table in which to perform the swap
        :param str db_path: path to the database

        :raises IndexError: invalid index
        :raises IOError: cannot open file
        :raises OSError: error writing to database
        :raises TypeError: invalid index type
        :raises Exception: field does not exist 
    """
    try:
        if not exists_table(table_name, db_path):
            raise Exception('Table %s does not exist' % table_name)

        db_file = codecs.open(db_path, 'r', 'utf-8')
        db_data = json.load(db_file)
        db_file.close()

        temp = db_data[codecs.decode(table_name, 'utf-8')]['fields'][index1]
        db_data[codecs.decode(table_name, 'utf-8')]['fields'][index1] =\
                db_data[codecs.decode(table_name, 'utf-8')]['fields'][index2]
        db_data[codecs.decode(table_name, 'utf-8')]['fields'][index2] = temp

        db_file = codecs.open(db_path, 'w', 'utf-8')
        db_file.write(json.dumps(db_data, ensure_ascii=False,
                sort_keys=True, indent=4))
        db_file.close()

    except IndexError as e:
        raise e
    except IOError as e:
        raise e
    except OSError as e:
        raise e
    except TypeError as e:
        raise e

