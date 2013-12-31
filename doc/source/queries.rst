Queries
=======

********
Overview
********

Since version **1.1.0**, it is possible to run queries from within breezedb to perform operations in a database. Queries are **strings** that follow a specific syntax depeneding on the operation and can be concatenated with other queries to run subsequently by separating them with **>>**.

As of version **1.2.0**, the available query types are:

- CREATE_
- EMPTY_
- EXISTS_
- GET_
- MODIFY_
- REMOVE_
- RENAME_
- SEARCH_
- SWAP_

Note that the syntax of the query varies slightly depending on the level of the database it is aiming for (database, table, field or element). Usually, the word before each argument indicates its level:

- **AT** -> database
- **IN** -> table
- **FROM/OF** -> field

Arguments must be specified between **% %;**. In order to run a query, simply call the following function:

>>> import breezedb
>>> breezedb.run_query("QUERY_HERE")

Alternatively, you may also want to store the query, or queries, in a variable for later use.

>>> import breezedb
>>> myquery = "QUERY1>>QUERY2>>QUERY3"
>>> breezedb.run_query(myquery)

Note that there are no spaces between the **>>** characters.

.. _CREATE:

*****************
CREATE operations
*****************

The creation queries can be used to create **databases**, **tables**, **fields** and **element rows**.

Database creation
#################

The syntax for this operation is as follows::

    CREATE DB %dbname%; AT %path%;

This will create a new directory called *dbname* in the specified *path*

Table creation
##############

The syntax for this operation is as follows::

    CREATE TABLE %table1%; %table2%; %table3%; AT %dbpath%;

This will create tables in the database located in *dbpath*. Note that it is possible to include as many tables as desired.

Field creation
##############

The syntax for this operation is as follows::

    CREATE FIELD %field1%; %type1%; %field2%; %type2%; IN %table%; AT %dbpath%;

This will create fields in the specified *table*. Note that it is possible to include as many fields as desired.

The available data types are:

    'str' -> strings
    'int' -> integer numbers
    'float' -> float numbers
    'bool' -> boolean statements (represented as 0 for false and 1 for true)

Row creation
############

The syntax for this operation is as follows::

    CREATE ROW %element1%; %element2%; %element3%; IN %table%; AT %dbpath%;

This will create a new data row in the specified *table*. The number of element arguments **must be the number of fields present in the table**.

.. _EMPTY:

****************
EMPTY operations
****************

It is possible to empty a **field** or **element/row** of the database.

Emptying a field in the whole table
###################################

The syntax for this operation is as follows::

    EMPTY FIELD %field1%; %field2%; %field3%; IN %table%; AT %dbpath%;

This will empty the contents of the specified fields in all the *table*. Note that it is possible to include as many fields as desired.

Emptying the field of a row
###########################

The syntax for this operation is as follows::

    EMPTY FIELD %field1%; %field2%; %field3%; OF %index%; AT %dbpath%;

This will empty the contents of the specified fields in a specific row *index*. Note that it is possible to include as many fields as desired.

Emptying an element
###################

The syntax for this operation is as follows::

    EMPTY ELEMENT %index1%; %index2%; %index3%; FROM %field%; IN %table%; AT %dbpath%;

This will empty the contents of the specified fields. Note that it is possible to include as many indexes as desired.

.. _EXISTS:

*****************
EXISTS operations
*****************

It is possible to check if a **table**, **field** or **row** exist in the database.

Check if a table exists
#######################

The syntax for this operation is as follows::

    EXISTS TABLE %table%; AT %dbpath%;

This will determine whether the *table* exists in the database or not.

Check if a field exists
#######################

The syntax for this operation is as follows::

    EXISTS FIELD %field%; IN %table%; AT %dbpath%;

This will determine whether the *field* exists in the *table* or not.

Check if an element exists
##########################

The syntax for this operation is as follows::

    EXISTS ELEMENT %index%; FROM %field%; IN %table%; AT %dbpath%;

This will determine whether the *element index* exists in the *field* or not.

.. _GET:

**************
GET operations
**************

The get queries can be used to get the contents of **databases**, **tables**, **fields** and **elements/rows**.

Obtain a list of tables
#######################

The syntax for this operation is as follows::

    GET TABLES AT %dbpath%;

This will return a list of tables present in the database at *dbpath*.

Obtain a list of fields
#######################

The syntax for this operation is as follows::

    GET FIELDS IN %table%; AT %dbpath%;

This will return a list of fields contained in the specified *table*.

Obtain the data type of a field
###############################

The syntax for this operation is as follows::

    GET TYPE OF %field%; IN %table%; AT %dbpath%;

This will return the *type* of the selected field. This is mainly used to know how to parse the elements of that field.

Obtain a list of elements
#########################

The syntax for this operation is as follows::

    GET ELEMENTS FROM %field%; IN %table%; AT %dbpath%;

This will return a list of element rows in the specified *field*.

Obtain the contents of a row
############################

The syntax for this operation is as follows::

    GET ROW %index%; IN %table%; AT %dbpath%;

This will return the data row of the *table* in the position specified by *index*. The data presented is ordered by priority of the fields.

Obtain a complete list of rows
##############################

The syntax for this operation is as follows::

    GET ROWS IN %table%; AT %dbpath%;

This will return a list of dictionaries that represent each row contained in the *table*. Note that the data in these dictionaries may not be ordered by priority.

Obtain the content of an element
################################

The syntax for this operation is as follows::

    GET ELEMENT %index%; FROM %field%; IN %table%; AT %dbpath%;

This will return the data contained in a specific element of the *table* in the position specified by *index*.

.. _MODIFY:

****************
MODIFY operation
****************

This operation is used to modify the content of a specific element, instead of the complete data row, of a given field::

    MODIFY %index%; FROM %field%; IN %table%; AT %dbpath%; TO %;new content%;

This will modify the content in the given index to *new content*.

.. _REMOVE:

*****************
REMOVE operations
*****************

The removal queries can be used to remove the contents of **databases**, **tables**, **fields** and **elements/rows**.

Removing a database
###################

The syntax for this operation is as follows::

    REMOVE DB AT %dbpath%;

This will delete the database located in *dbpath*.

Removing a table
################

The syntax for this operation is as follows::

    REMOVE TABLE %table1%; %table2%; %table3%; AT %dbpath%;

This will remove the specified tables in the database located in *dbpath*. Note that it is possible to include as many tables as desired.

Removing a field
################

The syntax for this operation is as follows::

    REMOVE FIELD %field1%; %field2%; %field3%; IN %table%; AT %dbpath%;

This will remove the specified fields in the *table*. Note that it is possible to include as many fields as desired.

Removing a data row
###################

The syntax for this operation is as follows::

    REMOVE ROW %index1%; %index2%; %index3%; IN %table%; AT %dbpath%;

This will remove the specified data rows in the *table*. Note that it is possible to include as many row indexes as desired.

.. _RENAME:

*****************
RENAME operations
*****************

The renaming queries can be used to rename **tables** and **fields**.

Renaming a table
################

The syntax for this operation is as follows::

    RENAME TABLE %actual name%; AT %dbpath%; TO %new name%;

This will substitute the name of the specified table to *new name*.

Renaming a field
################

The syntax for this operation is as follows::

   RENAME FIELD %actual name%; IN %table%; AT %dbpath%; TO %new name%;

This will substitute the name of the specified field to *new name*.

.. _SEARCH:

*****************
SEARCH operations
*****************

The SEARCH operations ignore the case of the content by default.

Searching the whole table
#########################

The operation is used to search for specific content in the whole table::

    SEARCH %data%; IN %table%; AT %dbpath%

This will return a list of indexes matching the content searched.

Searching a specific field
##########################

The operation is used to search for specific content in a specific field of the table::

    SEARCH %data%; FROM %field%; IN %table%; AT %dbpath%; 

This will return a list of indexes matching the content searched.

.. _SWAP:

**************
SWAP operation
**************

The SWAP operation is used to alter the priority of fields in the table::

    SWAP FIELD %index1%; WITH %index2%; IN %table%; AT %dbpath%; 

This will make *index2* have the priority that *index1* had and viceversa.

