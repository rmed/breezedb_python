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
.. module:: query
    :platform: Unix, Windows
    :synopsis: Query parsing for breezedb.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import breezedb, re

# Regular expression pattern
PATTERN = "(\w+|'.*?')"

class Parser():
    """ Parses the query and performs actions accordingly.

        :arg str query: query to parse
    """

    def __init__(self, query):
        self.queries = query.split(';')

    def run(self):
        """ Run the queries. """
        #TODO

def run_query(query):
    """ Parse and execute a query in the database.
    
        :param str query: query to execute
    """
    parser = Parser(query)
    parser.run()

