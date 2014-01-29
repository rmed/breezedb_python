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
.. module:: parser
    :platform: UNIX, Windows
    :synopsis: DB parsing.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import codecs, json, os

def read(db_path):
    """ Read a database file in the specified path.

        :param str db_path: complete path to the database file
        :returns: data contained in the file
    """
    db_file = codecs.open(db_path, 'r', 'utf-8')
    db_data = json.load(db_file, encoding='utf-8')
    db_file.close()

    return db_data

def write(db_path, db_data):
    """ Write data to a database.

        :param str db_path: complete path to the database file
        :param data: new data to store in the database
    """
    db_file = codecs.open(db_path, 'w', 'utf-8')
    db_file.write(json.dumps(db_data, ensure_ascii=False,
            sort_keys=True, indent=4))
    db_file.close()

