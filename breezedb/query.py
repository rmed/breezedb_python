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
from breezedb.breeze_exceptions import BreezeException

# Regular expression pattern
PATTERN = "(\w+|'.*?')"

class Parser():
    """ Parses the query and divides it into subqueries where possible.

        :arg str query: query to parse
    """

    def __init__(self, query):
        self.query = query
        self.elements = re.findall(PATTERN, query)

    def run(self):
        """ Run the query. """
        # Check the type of operation
        if self.elements[0] == "CREATE":
            self.create()
        
    def create(self):
        """ Run a CREATE operation. 
            
            First check the database level and then call the function
        """
        level = self.elements[1]
        database = self.elements[-1]

        if level == 'DB':
            name = self.elements[2].strip("'")
            breezedb.create_db(database, name)
        
        elif level == 'TABLE':
            tablelist = []
            for element in self.elements[2:]:
                if element != 'AT':
                    tablelist.append(element.strip("'"))
                else:
                    break
            for table in tablelist:
                breezedb.create_table(table, database)

        elif level == 'FIELD':
            table = self.elements[-3]
            fieldlist = []
            for index, element in enumerate(self.elements[2:-1:2]):
                if element != 'IN' and self.elements[index + 1] \
                    in breezedb.field.TYPES:
                    field = [element, self.elements[index + 1]]
                    fieldlist.append(field)
                else:
                    break
            for field in fieldlist:
                    breezedb.create_field(field[0], field[1], table, database)

        elif level == 'ELEMENT':
            table = self.elements[-3]
            elementlist = []
            for element in self.elemets[2:]:
                if element != 'IN':
                    elementlist.append(element)
                else:
                    break
            breezedb.create_element_row(elementlist, table, database)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

def run_query(query):
    """ Parse and execute a query in the database.
        
        This function divides the query (if there are more than one) by
        using the ';' symbol and then runs a parser for each one.
    
        :param str query: query to execute
    """
    query_list = query.split(';')
    for subquery in query_list:
        parser = Parser(subquery)
        parser.run()
