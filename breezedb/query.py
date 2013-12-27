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
.. module:: query
    :platform: Unix, Windows
    :synopsis: Query parsing for breezedb.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import re
from db import *
from table import *
from field import *
from element import *

# Regular expression for arguments
RE_ARG = re.compile('%(.+?)%;')

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
        elif re.match("EMPTY (.*)", self.query):
            self.empty()
        elif re.match("EXISTS (.*)", self.query):
            return self.exists()
        elif re.match("GET (.*)", self.query):
            return self.get()
        elif re.match("MODIFY (.*)", self.query):
            self.modify()
        elif re.match("REMOVE (.*)", self.query):
            self.remove()
        elif re.match("RENAME (.*)", self.query):
            self.rename()
        elif re.match("SEARCH (.*)", self.query):
            return self.search()
        elif re.match("SWAP (.*)", self.query):
            self.swap()
        else:
            raise Exception('Invalid query: %s' % self.query)
            
    def create(self):
        """ Run a CREATE operation. This operation works with databases,
            tables and fields.

            :raises Exception: incorrect query syntax, incorrect number of parameters          
        """
        re_create_db = re.compile("CREATE DB %(.+?)%; AT %(.+?)%;")
        re_create_table = re.compile("CREATE TABLE (.*) AT %(.+?)%;")
        re_create_field = re.compile("CREATE FIELD (.*) IN %(.+?)%; AT %(.+?)%;")
        re_create_row = re.compile("CREATE ROW (.*) IN %(.+?)%; AT %(.+?)%;")

        if re_create_db.match(self.query):
            # CREATE DB %name%; AT %path%;
            db_name = re_create_db.match(self.query).group(1)
            db_path = re_create_db.match(self.query).group(2)
            create_db(db_path, db_name)
        
        elif re_create_table.match(self.query):
            # CREATE TABLE %table1%; %table2%; ...  AT %db%;
            table_args = re_create_table.match(self.query).group(1)
            db_path = re_create_table.match(self.query).group(2)
            table_list = RE_ARG.findall(table_args)

            for t in table_list:
                create_table(t, db_path)

        elif re_create_field.match(self.query):
            # CREATE FIELD %name1%; %type1%; %name2%; %type2%; ... IN %table%; AT %db%;
            field_args = re_create_field.match(self.query).group(1)
            table_name = re_create_field.match(self.query).group(2)
            db_path = re_create_field.match(self.query).group(3)
            field_list = RE_ARG.findall(field_args)

            if len(field_list)%2 != 0:
                raise Exception('Number of passed arguments is not correct')

            it = 0
            while it < len(field_list):
                create_field(field_list[it], field_list[it+1], table_name,
                        db_path)
                it += 2

        elif re_create_row.match(self.query):
            # CREATE ROW %element%; %element%; ... IN %table%; AT %db%;
            element_args = re_create_row.match(self.query).group(1)
            table_name = re_create_row.match(self.query).group(2)
            db_path = re_create_row.match(self.query).group(3)
            element_list = RE_ARG.findall(element_args)

            create_row(element_list, table_name, db_path)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def empty(self):
        """ Run an EMPTY operation. This operation works with fields and
            elements.

            :raises Exception: incorrect query syntax 
        """
        re_empty_field = re.compile("EMPTY FIELD (.*) IN %(.+?)%; AT %(.+?)%;")
        re_empty_field_row = re.compile("EMPTY FIELD (.*) OF %(.+?)%; IN %(.+?)%; AT %(.+?)%;")
        re_empty_element = re.compile("EMPTY ELEMENT (.*) FROM %(.+?)%; IN %(.+?)%; AT %(.+?)%;")

        if re_empty_field.match(self.query):
            # EMPTY FIELD %field1%; %field2%; ... IN %table%; AT %db%; 
            field_args = re_empty_field.match(self.query).group(1)
            table_name = re_empty_field.match(self.query).group(2)
            db_path = re_empty_field.match(self.query).group(3)
            field_list = RE_ARG.findall(field_args)

            for f in field_list:
                empty_field_table(f, table_name, db_path)

        elif re_empty_field_row.match(self.query):
            # EMPTY FIELD %field1%; %field2%; ... OF %index%; IN %table%; AT %db%; 
            field_args = re_empty_field_row.match(self.query).group(1)
            index = int(re_empty_field_row.match(self.query).group(1))
            table_name = re_empty_field_row.match(self.query).group(3)
            db_path = re_empty_field_row.match(self.query).group(4)
            field_list = RE_ARG.findall(field_args)

            for f in field_list:
                empty_field_row(index, f, table_name, db_path)

        elif re_empty_element.match(self.query):
            # EMPTY ELEMENT %index1%; %index2%; ... FROM %field%; IN %table%; AT %db%; 
            index_args = re_empty_element.match(self.query).group(1)
            field_name = re_empty_element.match(self.query).group(2)
            table_name = re_empty_element.match(self.query).group(3)
            db_path = re_empty_element.match(self.query).group(4)
            index_list = RE_ARG.findall(index_args)

            for index in index_list:
                empty_element(int(index), field, table, database)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def exists(self):
        """ Run an EXISTS operation. This operation works with tables,
            fields and rows.

            :returns: True or False

            :raises Exception: incorrect query syntax 
        """
        re_exists_table = re.compile("EXISTS TABLE %(.+?)%; AT %(.+?)%;")
        re_exists_field = re.compile("EXISTS FIELD %(.+?)%; IN %(.+?)%; AT %(.+?)%;")
        re_exists_row = re.compile("EXISTS ROW %(.+?)%; IN %(.+?)%; AT %(.+?)%;")

        if re_exists_table.match(self.query):
            # EXISTS TABLE %table%; AT %db%; 
            table_name = re_exists_table.match(self.query).group(1)
            db_path = re_exists_table.match(self.query).group(2)

            return exists_table(table_name, db_path)

        elif re_exists_field.match(self.query):
            # EXISTS FIELD %field%; IN %table%; AT %db%; 
            field_name = re_exists_field.match(self.query).group(1)
            table_name = re_exists_field.match(self.query).group(2)
            db_path = re_exists_field.match(self.query).group(3)

            return exists_field(field_name, table_name, db_path)

        elif re_exists_row.match(self.query):
            # EXISTS ROW %index%; IN %table%; AT %db%; 
            index = int(re_exists_row.match(self.query).group(1))
            table_name = re_exists_row.match(self.query).group(2)
            db_path = re_exists_row.match(self.query).group(3)

            return exists_row(index, field_name, table_name, db_path)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def get(self):
        """ Run a GET operation. This operation works with databases,
            tables, fields and elements.

            :returns: list of results obtained from the query

            :raises Exception: incorrect query syntax
        """
        re_get_tables = re.compile("GET TABLES AT %(.+?)%;")
        re_get_fields = re.compile("GET FIELDS IN %(.+?)%; AT %(.+?)%;")
        re_get_type = re.compile("GET TYPE OF %(.+?)%; IN %(.+?)%; AT %(.+?)%;")
        re_get_elements = re.compile("GET ELEMENTS FROM %(.+?)%; IN %(.+?)%; AT %(.+?)%;")
        re_get_row = re.compile("GET ROW %(.+?)%; IN %(.+?)%; AT %(.+?)%;")
        re_get_element = re.compile("GET ELEMENT %(.+?)%; FROM %(.+?)%; IN %(.+?)%; AT %(.+?)%;")

        if re_get_tables.match(self.query):
            # GET TABLES AT %db%; 
            db_path = re_get_tables.match(self.query).group(1)

            return get_table_list(db_path)

        elif re_get_fields.match(self.query):
            # GET FIELDS IN %table%; AT %db%; 
            table_name = re_get_fields.match(self.query).group(1)
            db_path = re_get_fields.match(self.query).group(2)
            
            return get_field_list(table_name, db_path)

        elif re_get_type.match(self.query):
            # GET TYPE OF %field%; IN %table%; AT %db$;
            field_name = re_get_type.match(self.query).group(1)
            table_name = re_get_type.match(self.query).group(2)
            db_path = re_get_type.match(self.query).group(3)

            return get_field_type(field_name, table_name, db_path)

        elif re_get_elements.match(self.query): 
            # GET ELEMENTS FROM %field%; IN %table%; AT %db%; 
            field_name = re_get_elements.match(self.query).group(1)
            table_name = re_get_elements.match(self.query).group(2)
            db_path = re_get_elements.match(self.query).group(3)
            
            return get_field_data(field_name, table_name, db_path)

        elif re_get_row.match(self.query):
            # GET ROW %index%; IN %table%; AT %db%; 
            index = int(re_get_row.match(self.query).group(1))
            table_name = re_get_row.match(self.query).group(2)
            db_path = re_get_row.match(self.query).group(3)

            return get_row(index, table_name, db_path)

        elif re_get_element.match(self.query):
            # GET ELEMENT %index%; FROM %field%; IN %table%; AT %db%; 
            index = int(re_get_element.match(self.query).group(1))
            field_name = re_get_element.match(self.query).group(2)
            table_name = re_get_element.match(self.query).group(3)
            db_path = re_get_element.match(self.query).group(4)

            return get_element_data(index, field_name, table_name, db_path)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def modify(self):
        """ Run a MODIFY operation. This operation only works with elements. 

            :raises Exception: incorrect query syntax 
        """
        re_modify = re.compile("MODIFY %(.+?)%; FROM %(.+?)%; IN %(.+?)%; AT %(.+?)%; TO %(.+?)%;")

        if re_modify.match(self.query):
            # MODIFY %index%; FROM %field%; IN %table%; AT %db%; TO %new content""
            index = int(re_modify.match(self.query).group(1))
            field_name = re_modify.match(self.query).group(2)
            table_name = re_modify.match(self.query).group(3)
            db_path = re_modify.match(self.query).group(4)
            new_content = re_modify.match(self.query).group(5)

            modify_element(index, field_name, table_name, db_path, new_content)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def remove(self):
        """ Run a REMOVE operation. This operation works with databases,
            tables, fields and elements.

            :raises Exception: incorrect query syntax
        """
        re_remove_db = re.compile("REMOVE DB AT %(.+?)%;")
        re_remove_table = re.compile("REMOVE TABLE (.*) AT %(.+?)%;")
        re_remove_field = re.compile("REMOVE FIELD (.*) IN %(.+?)%; AT %(.+?)%;")
        re_remove_row = re.compile("REMOVE ROW (.*) IN %(.+?)%; AT %(.+?)%;")

        if re_remove_db.match(self.query):
            # REMOVE DB AT %path""
            db_path = re_remove_db.match(self.query).group(1)

            remove_db(db_path)

        elif re_remove_table.match(self.query):
            # REMOVE TABLE %table1%; %table2%; ... AT %db%; 
            table_args = re_remove_table.match(self.query).group(1)
            db_path = re_remove_table.match(self.query).group(2)
            table_list = RE_ARG.findall(table_args)

            for t in table_list:
                remove_table(t, db_path)

        elif re_remove_field.match(self.query):
            # REMOVE FIELD %field1%; %field2%; ... IN %table%; AT %db%; 
            field_args = re_remove_field.match(self.query).group(1)
            table_name = re_remove_field.match(self.query).group(2)
            db_path = re_remove_field.match(self.query).group(3)
            field_list = RE_ARG.findall(field_args)

            for f in field_list:
                remove_field(f, table_name, db_path)

        elif re_remove_row.match(self.query):
            # REMOVE ROW %index1%; %index2%; ... IN %table%; AT %db%; 
            index_args = re_remove_row.match(self.query).group(1)
            table_name = re_remove_row.match(self.query).group(2)
            db_path = re_remove_row.match(self.query).group(3)
            index_list = RE_ARG.findall(index_args)

            for index in index_list:
                remove_row(int(index), table_name, db_path)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def rename(self):
        """ Run a RENAME operation. This operation works with tables and
            fields.

            :raises Exception: incorrect query syntax
        """
        re_rename_table = re.compile("RENAME TABLE %(.+?)%; AT %(.+?)%; TO %(.+?)%;")
        re_rename_field = re.compile("RENAME FIELD %(.+?)%; IN %(.+?)%; AT %(.+?)%; TO %(.+?)%;")

        if re_rename_table.match(self.query) :
            # RENAME TABLE %name%; AT %db%; TO %new name""
            table_name = re_rename_table.match(self.query).group(1)
            db_path = re_rename_table.match(self.query).group(2)
            new_name = re_rename_table.match(self.query).group(3)

            rename_table(table_name, db_path, new_name)
        
        elif re_rename_field.match(self.query):
            # RENAME FIELD %name%; IN %table%; AT %db%; TO %new name""
            field_name = re_rename_field.match(self.query).group(1)
            table_name = re_rename_field.match(self.query).group(2)
            db_path = re_rename_field.match(self.query).group(3)
            new_name = re_rename_field.match(self.query).group(4)

            rename_field(field_name, table_name, db_path, new_name)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def search(self):
        """ Run a SEARCH operation.

            :returns: list of results obtained from the query

            :raises Exception: incorrect query syntax 
        """
        re_search = re.compile("FIND %(.+?)%; IN %(.+?)%; AT %(.+?)%;")
        re_search_field = re.compile("FIND %(.+?)%; FROM %(.+?)%; IN %(.+?)%; AT %(.+?)%;")

        if re_find.match(self.query):
            # SEARCH %data%; IN %table%; AT %db%; 
            data = re_search.match(self.query).group(1)
            table_name = re_search.match(self.query).group(2)
            db_path = re_search.match(self.query).group(3)

            return search_data(data, table_name, db_path)

        elif re_find.match(self.query):
            # SEARCH %data%; FROM %field%; IN %table%; AT %db%; 
            data = re_search_field.match(self.query).group(1)
            field_name = re_search_field.match(self.query).group(2)
            table_name = re_search_field.match(self.query).group(3)
            db_path = re_search_field.match(self.query).group(4)

            return search_data(data, table_name, db_path, field_name)

        else:
            raise Exception('Invalid query: %s' % self.query)

    def swap(self):
        """ Run a SWAP operation. This operation only works with fields.

            :raises Exception: incorrect query syntax
        """
        re_swap = re.compile("SWAP FIELD %(.+?)%; WITH %(.+?)%; IN %(.+?)%; AT %(.+?)%;")

        if re_swap.match(self.query):
            # SWAP FIELD %index1%; WITH %index2%; IN %table%; AT %db%; 
            index1 = int(re_swap.match(self.query).group(1))
            index2 = int(re_swap.match(self.query).group(2))
            table_name = re_swap.match(self.query).group(3)
            db_path = re_swap.match(self.query).group(4)

            swap_fields(index1, index2, table_name, db_path)

        else:
            raise Exception('Invalid query: %s' % self.query)

def run_query(query):
    """ Parse and execute a query in the database.
        
        This function divides the query (if there are more than one) by
        using the string '>>' and then runs a parser for each one.
    
        :param str query: query to execute
    """
    query_list = query.split('>>')
    result_list = []
    for subquery in query_list:
        parser = Parser(subquery)
        result = parser.run()
        if result:
            result_list.append(result)
    
    # Results must be parsed manually
    if result_list:
        return result_list

