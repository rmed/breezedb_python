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
        operation = self.elements[0]
        if operation == 'CREATE':
            self.create()
        elif operation == 'GET':
            return self.get()
        elif operation == 'REMOVE':
            self.remove()
        elif operation == 'RENAME':
            self.rename()
        elif operation == 'EXISTS':
            return self.exists()
        elif operation == 'EMPTY':
            self.empty()
        elif operation == 'FIND':
            return self.find()
        elif operation == 'MODIFY':
            self.modify()
        else:
            return
        
    def create(self):
        """ Run a CREATE operation. This operation works with databases,
            tables and fields.

            :raises BreezeException: incorrect query syntax           
        """
        level = self.elements[1]
        database = normalize(self.elements[-1])

        if level == 'DB':
            # CREATE DB 'name' AT 'path'
            name = normalize(self.elements[2])
            breezedb.create_db(database, name)
        
        elif level == 'TABLE':
            # CREATE TABLE 'name' AT 'db'
            tablelist = []
            for element in self.elements[2:]:
                if element != 'AT':
                    tablelist.append(normalize(element))
                else:
                    break
            for table in tablelist:
                breezedb.create_table(table, database)

        elif level == 'FIELD':
            # CREATE FIELD 'name' 'type' 'name' 'type' ... IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            fieldlist = []
            it = 2
            while self.elements[it] != 'IN':
                if normalize(self.elements[it + 1]) in breezedb.TYPES:
                    field = [normalize(self.elements[it]),\
                        normalize(self.elements[it + 1])]
                    fieldlist.append(field)
                else:
                    break
                it += 2

            for field in fieldlist:
                    breezedb.create_field(field[0], field[1], table, database)

        elif level == 'ELEMENTS':
            # CREATE ELEMENTS 'element', 'element',... IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            elementlist = []
            for element in self.elements[2:]:
                if element != 'IN':
                    elementlist.append(normalize(element))
                else:
                    break
            breezedb.create_element_row(elementlist, table, database)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

    def get(self):
        """ Run a GET operation. This operation works with tables, fields
            and elements.

            :returns: list of results obtained from the query

            :raises BreezeException: incorrect query syntax 
        """
        level = self.elements[1]
        database = normalize(self.elements[-1])

        if level == 'TABLES':
            # GET TABLES AT 'db'
            return breezedb.get_table_list(database)

        elif level == 'FIELDS':
            # GET FIELDS IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            return breezedb.get_field_list(table, database)

        elif level == 'TYPE':
            # GET TYPE OF 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[3])
            return breezedb.get_field_type(field, table, database)

        elif level == 'ELEMENTS' and self.elements[2] == 'FROM':
            # GET ELEMENTS FROM 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[-5])
            return breezedb.get_element_list(field, table, database)

        elif level == 'ROW':
            # GET ROW 'index' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            row = int(normalize(self.elements[2]))
            return breezedb.get_element_row(row, table, database)

        elif level == 'ELEMENT':
            # GET ELEMENT 'index' FROM 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[-5])
            index = int(normalize(self.elements[2]))
            return breezedb.get_element_content(index, field, table, database)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

    def remove(self):
        """ Run a REMOVE operation. This operation works with databases,
            tables, fields and elements.

            :raises BreezeException: incorrect query syntax 
        """
        level = self.elements[1]
        database = normalize(self.elements[-1])

        if level == 'DB':
            # REMOVE DB AT 'path'
            breezedb.remove_db(database)

        elif level == 'TABLE':
            # REMOVE TABLE 'name' AT 'db'
            table = normalize(self.elements[-3])
            breezedb.remove_table(table, database)

        elif level == 'FIELD':
            # REMOVE FIELD 'name' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[2])
            breezedb.remove_field(field, table, database)

        elif level == 'ROW':
            # REMOVE ROW 'index' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            index = int(normalize(self.elements[2]))
            breezedb.remove_element_row(index, table, database)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

    def rename(self):
        """ Run a RENAME operation. This operation works with tables and
            fields.

            :raises BreezeException: incorrect query syntax 
        """
        level = self.elements[1]
        database = normalize(self.elements[-3])
        new_name = normalize(self.elements[-1])

        if level == 'TABLE':
            # RENAME TABLE 'name' AT 'db' TO 'new name'
            table = normalize(self.elements[2])
            breezedb.rename_table(table, database, new_name)
        
        elif level == 'FIELD':
            # RENAME FIELD 'name' IN 'table' AT 'db' TO 'new name'
            field = normalize(self.elements[2])
            table = normalize(self.elements[4])
            breezedb.rename_field(field, table, database, new_name)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

    def exists(self):
        """ Run an EXISTS operation. This operation works with tables,
            fields and elements.

            :returns: True or False

            :raises BreezeException: incorrect query syntax 
        """
        level = self.elements[1]
        database = normalize(self.elements[-1])

        if level == 'TABLE':
            # EXISTS TABLE 'table' AT 'db'
            table = normalize(self.elements[-3])
            return breezedb.table_exists(table, database)

        if level == 'FIELD':
            # EXISTS FIELD 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[2])
            return breezedb.field_exists(field, table, database)

        if level == 'ELEMENT':
            # EXISTS ELEMENT 'index' FROM 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[-5])
            index = int(normalize(self.elements[2]))
            return breezedb.element_exists(index, field, table, database)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

    def empty(self):
        """ Run an EMPTY operation. This operation works with fields and
            elements.

            :raises BreezeException: incorrect query syntax 
        """
        level = self.elements[1]
        database = normalize(self.elements[-1])

        if level == 'FIELD':
            # EMPTY FIELD 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[2])
            breezedb.empty_field(field, table, database)

        elif level == 'ELEMENT':
            # EMPTY ELEMENT 'index' FROM 'field' IN 'table' AT 'db'
            table = normalize(self.elements[-3])
            field = normalize(self.elements[-5])
            index = int(normalize(self.elements[2]))
            breezedb.empty_element(index, field, table, database)

        else:
            raise BreezeException('query', 'incorrect syntax: %s' %self.query)

    def find(self):
        """ Run a FIND operation. This operation only works with elements.

            :returns: list of results obtained from the query

            :raises BreezeException: incorrect query syntax 
        """
        # FIND 'content' FROM 'field' IN 'table' AT 'db'
        database = normalize(self.elements[-1])
        table = normalize(self.elements[-3])
        field = normalize(self.elements[-5])
        content = normalize(self.elements[1])
        return breezedb.find_element(content, field, table, database)

    def modify(self):
        """ Run a MODIFY operation. This operation only works with elements. 

            :raises BreezeException: incorrect query syntax 
        """
        # MODIFY 'index' FROM 'field' IN 'table' AT 'db' TO 'new content'
        new_content = normalize(self.elements[-1])
        database = normalize(self.elements[-3])
        table = normalize(self.elements[-5])
        field = normalize(self.elements[3])
        index = int(normalize(self.elements[1]))
        breezedb.modify_element(index, field, table, database, new_content)

def normalize(element):
    """ Remove the ' symbols of an element (if any)

        :param str element: element to normalize
    
        :returns: normalized element
    """
    return element.strip("'")

def run_query(query):
    """ Parse and execute a query in the database.
        
        This function divides the query (if there are more than one) by
        using the ';' symbol and then runs a parser for each one.
    
        :param str query: query to execute
    """
    query_list = query.split(';')
    for subquery in query_list:
        parser = Parser(subquery)
        return parser.run()

