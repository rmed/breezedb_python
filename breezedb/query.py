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

class Parser():
    """ Parses the query and divides it into subqueries where possible.

        :arg str query: query to parse
    """

    def __init__(self, query):
        self.query = query

    def run(self):
        """ Run the query. """
        # Check the type of operation
        if re.match("CREATE (.*)", self.query):
            self.create()
        elif re.match("GET (.*)", self.query):
            return self.get()
        elif re.match("REMOVE (.*)", self.query):
            self.remove()
        elif re.match("RENAME (.*)", self.query):
            self.rename()
        elif re.match("EXISTS (.*)", self.query):
            return self.exists()
        elif re.match("EMPTY (.*)", self.query):
            self.empty()
        elif re.match("FIND (.*)", self.query):
            return self.find()
        elif re.match("MODIFY (.*)", self.query):
            self.modify()
        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)
            
    def create(self):
        """ Run a CREATE operation. This operation works with databases,
            tables and fields.

            :raises BreezeException: incorrect query syntax           
        """
        re_create_db = re.compile("CREATE DB \'(.*?)\' AT \'(.*?)\'")
        re_create_table = re.compile("CREATE TABLE (.*) AT \'(.*?)\'")
        re_create_field = re.compile("CREATE FIELD (.*) IN \'(.*?)\' AT \'(.*?)\'")
        re_create_elements = re.compile("CREATE ELEMENTS (.*) IN \'(.*?)\' AT \'(.*?)\'")
        re_arg = re.compile("\'(.*?)\'")

        if re_create_db.match(self.query):
            # CREATE DB 'name' AT 'path'
            db_name = re_create_db.match(self.query).group(1)
            db_path = re_create_db.match(self.query).group(2)
            breezedb.create_db(db_path, db_name)
        
        elif re_create_table.match(self.query):
            # CREATE TABLE 'table1' 'table2' ...  AT 'db'
            table_args = re_create_table.match(self.query).group(1)
            db_path = re_create_table.match(self.query).group(2)
            tablelist = re_arg.findall(table_args)

            for table in tablelist:
                breezedb.create_table(table, db_path)

        elif re_create_field.match(self.query):
            # CREATE FIELD 'name' 'type' 'name' 'type' ... IN 'table' AT 'db'
            field_args = re_create_field.match(self.query).group(1)
            table_name = re_create_field.match(self.query).group(2)
            db_path = re_create_field.match(self.query).group(3)
            fieldlist = re_arg.findall(field_args)

            it = 0
            while it < len(fieldlist):
                    breezedb.create_field(fieldlist[it], fieldlist[it+1],
                            table_name, db_path)
                    it += 2

        elif re_create_elements.match(self.query):
            # CREATE ELEMENTS 'element', 'element',... IN 'table' AT 'db'
            element_args = re_create_elements.match(self.query).group(1)
            table_name = re_create_elements.match(self.query).group(2)
            db_path = re_create_elements.match(self.query).group(3)
            elementlist = re_arg.findall(element_args)

            breezedb.create_element_row(elementlist, table_name, db_path)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def get(self):
        """ Run a GET operation. This operation works with tables, fields
            and elements.

            :returns: list of results obtained from the query

            :raises BreezeException: incorrect query syntax 
        """
        re_get_tables = re.compile("GET TABLES AT \'(.*?)\'")
        re_get_fields = re.compile("GET FIELDS IN \'(.*?)\' AT \'(.*?)\'")
        re_get_type = re.compile("GET TYPE OF \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")
        re_get_elements = re.compile("GET ELEMENTS FROM \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")
        re_get_row = re.compile("GET ROW \'(\d)\' IN \'(.*?)\' AT \'(.*?)\'")
        re_get_element = re.compile("GET ELEMENT \'(\d)\' FROM \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")

        if re_get_tables.match(self.query):
            # GET TABLES AT 'db'
            db_path = re_get.tables.match(self.query).group(1)

            return breezedb.get_table_list(db_path)

        elif re_get_fields.match(self.query):
            # GET FIELDS IN 'table' AT 'db'
            table_name = re_get_fields.match(self.query).group(1)
            db_path = re_get_fields.match(self.query).group(2)
            
            return breezedb.get_field_list(table_name, db_path)

        elif re_get_type.match(self.query):
            # GET TYPE OF 'field' IN 'table' AT 'db'
            field_name = re_get_type.match(self.query).group(1)
            table_name = re_get_type.match(self.query).group(2)
            db_path = re_get_type.match(self.query).group(3)
            
            return breezedb.get_field_type(field_name, table_name, db_path)

        elif re_get_elements.match(self.query): 
            # GET ELEMENTS FROM 'field' IN 'table' AT 'db'
            field_name = re_get_elements.match(self.query).group(1)
            table_name = re_get_elements.match(self.query).group(2)
            db_path = re_get_elements.match(self.query).group(3)
            
            return breezedb.get_element_list(field_name, table_name, db_path)

        elif re_get_row.match(self.query):
            # GET ROW 'index' IN 'table' AT 'db'
            index = re_get_row.match(self.query).group(1)
            table_name = re_get_row.match(self.query).group(2)
            db_path = re_get_row.match(self.query).group(3)

            return breezedb.get_element_row(index, table_name, db_path)

        elif re_get_element.match(self.query):
            # GET ELEMENT 'index' FROM 'field' IN 'table' AT 'db'
            index = re_get_element.match(self.query).group(1)
            field_name = re_get_element.match(self.query).group(2)
            table_name = re_get_element.match(self.query).group(3)
            db_path = re_get_element.match(self.query).group(4)

            return breezedb.get_element_content(index, field_name,
                    table_name, db_path)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def remove(self):
        """ Run a REMOVE operation. This operation works with databases,
            tables, fields and elements.

            :raises BreezeException: incorrect query syntax 
        """
        re_remove_db = re.compile("REMOVE DB AT \'(.*?)\'")
        re_remove_table = re.compile("REMOVE TABLE \'(.*?)\' AT \'(.*?)\'")
        re_remove_field = re.compile("REMOVE FIELD \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")
        re_remove_row = re.compile("REMOVE ROW \'(\d)\' IN \'(.*?)\' AT \'(.*?)\'")

        if re_remove_db.match(self.query):
            # REMOVE DB AT 'path'
            db_path = re_remove_db.match(self.query).group(1)

            breezedb.remove_db(db_path)

        elif re_remove_table.match(self.query):
            # REMOVE TABLE 'name' AT 'db'
            table_name = re_remove_table.match(self.query).group(1)
            db_path = re_remove_table.match(self.query).group(2)

            breezedb.remove_table(table_name, db_path)

        elif re_remove_field.match(self.query):
            # REMOVE FIELD 'name' IN 'table' AT 'db'
            field_name = re_remove_field.match(self.query).group(1)
            table_name = re_remove_field.match(self.query).group(2)
            db_path = re_remove_field.match(self.query).group(3)

            breezedb.remove_field(field_name, table_name, db_path)

        elif re_remove_row.match(self.query):
            # REMOVE ROW 'index' IN 'table' AT 'db'
            index = re_remove_row.match(self.query).group(1)
            table_name = re_remove_row.match(self.query).group(2)
            db_path = re_remove_row.match(self.query).group(3)

            breezedb.remove_element_row(index, table_name, db_path)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def rename(self):
        """ Run a RENAME operation. This operation works with tables and
            fields.

            :raises BreezeException: incorrect query syntax 
        """
        re_rename_table = re.compile("RENAME TABLE \'(.*?)\' AT \'(.*?)\' TO \'(.*?)\'")
        re_rename_field = re.compile("RENAME FIELD \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\' TO \'(.*?)\'")

        if re_rename_table.match(self.query) :
            # RENAME TABLE 'name' AT 'db' TO 'new name'
            table_name = re_rename_table.match(self.query).group(1)
            db_path = re_rename_table.match(self.query).group(2)
            new_name = re_rename_table.match(self.query).group(3)

            breezedb.rename_table(table_name, db_path, new_name)
        
        elif re_rename_field.match(self.query):
            # RENAME FIELD 'name' IN 'table' AT 'db' TO 'new name'
            field_name = re_rename_field.match(self.query).group(1)
            table_name = re_rename_field.match(self.query).group(2)
            db_path = re_rename_field.match(self.query).group(3)
            new_name = re_rename_field.match(self.query).group(4)

            breezedb.rename_field(field_name, table_name, db_path, new_name)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def exists(self):
        """ Run an EXISTS operation. This operation works with tables,
            fields and elements.

            :returns: True or False

            :raises BreezeException: incorrect query syntax 
        """
        re_exists_table = re.compile("EXISTS TABLE \'(.*?)\' AT \'(.*?)\'")
        re_exists_field = re.compile("EXISTS FIELD \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")
        re_exists_element = re.compile("EXISTS ELEMENT \'(\d)\' FROM \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")

        if re_exists_table.match(self.query):
            # EXISTS TABLE 'table' AT 'db'
            table_name = re_exists_table.match(self.query).group(1)
            db_path = re_exists_table.match(self.query).group(2)

            return breezedb.table_exists(table_name, db_path)

        if re_exists_field.match(self.query):
            # EXISTS FIELD 'field' IN 'table' AT 'db'
            field_name = re_exists_field.match(self.query).group(1)
            table_name = re_exists_field.match(self.query).group(2)
            db_path = re_exists_field.match(self.query).group(3)

            return breezedb.field_exists(field_name, table_name, db_path)

        if re_exists_element.match(self.query):
            # EXISTS ELEMENT 'index' FROM 'field' IN 'table' AT 'db'
            index = re_exists_element.match(self.query).group(1)
            field_name = re_exists_element.match(self.query).group(2)
            table_name = re_exists_element.match(self.query).group(3)
            db_path = re_exists_element.match(self.query).group(4)

            return breezedb.element_exists(index, field_name, table_name,
                    db_path)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def empty(self):
        """ Run an EMPTY operation. This operation works with fields and
            elements.

            :raises BreezeException: incorrect query syntax 
        """
        re_empty_field = re.compile("EMPTY FIELD \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")
        re_empty_element = re.compile("EMPTY ELEMENT \'(\d)\' FROM \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")

        if re_empty_field.match(self.query):
            # EMPTY FIELD 'field' IN 'table' AT 'db'
            field_name = re_empty_field.match(self.query).group(1)
            table_name = re_empty_field.match(self.query).group(2)
            db_path = re_empty_field.match(self.query).group(3)

            breezedb.empty_field(field_name, table_name, db_path)

        elif re_empty_element.match(self.query):
            # EMPTY ELEMENT 'index' FROM 'field' IN 'table' AT 'db'
            index = re_empty_element.match(self.query).group(1)
            field_name = re_empty_element.match(self.query).group(2)
            table_name = re_empty_element.match(self.query).group(3)
            db_path = re_empty_element.match(self.query).group(4)

            breezedb.empty_element(index, field, table, database)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def find(self):
        """ Run a FIND operation. This operation only works with elements.

            :returns: list of results obtained from the query

            :raises BreezeException: incorrect query syntax 
        """
        re_find = re.compile("FIND \'(.*?)\' FROM \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\'")
 
        if re_find.match(self.query):
            # FIND 'content' FROM 'field' IN 'table' AT 'db'
            content = re_find.match(self.query).group(1)
            field_name = re_find.match(self.query).group(2)
            table_name = re_find.match(self.query).group(3)
            db_path = re_find.match(self.query).group(4)

            return breezedb.find_element(content, field_name, table_name, db_path)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

    def modify(self):
        """ Run a MODIFY operation. This operation only works with elements. 

            :raises BreezeException: incorrect query syntax 
        """
        re_modify = re.compile("MODIFY \'(\d)\' FROM \'(.*?)\' IN \'(.*?)\' AT \'(.*?)\' TO \'(.*?)\'")

        if re_modify.match(self.query):
            # MODIFY 'index' FROM 'field' IN 'table' AT 'db' TO 'new content'
            index = re_modify.match(self.query).group(1)
            field_name = re_modify.match(self.query).group(2)
            table_name = re_modify.match(self.query).group(3)
            db_path = re_modify.match(self.query).group(4)
            new_content = re_modify.match(self.query).group(5)

            breezedb.modify_element(index, field, table, database, new_content)

        else:
            raise BreezeException('query', 'invalid query: %s' % self.query)

def run_query(query):
    """ Parse and execute a query in the database.
        
        This function divides the query (if there are more than one) by
        using the string ';;' and then runs a parser for each one.
    
        :param str query: query to execute
    """
    query_list = query.split(';;')
    for subquery in query_list:
        parser = Parser(subquery)
        return parser.run()

