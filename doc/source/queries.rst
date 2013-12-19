Queries
=======

********
Overview
********

Since version **1.1.0**, it is possible to run queries from within breezedb to perform operations in a database. Queries are **strings** that follow a specific syntax depeneding on the operation and can be concatenated with other queries to run subsequently by separating them with **;;**.

The available query types are:

- CREATE_
- GET_
- REMOVE_
- RENAME_
- EXISTS_
- EMPTY_
- FIND_
- MODIFY_

Note that the syntax of the query varies slightly depending on the level of the database it is aiming for (database, table, field or element). Usually, the word before each argument indicates its level:

- **AT** -> database
- **IN** -> table
- **FROM/OF** -> field

Arguments must be specified between **' '**. In order to run a query, simply call the following function:

>>> import breezedb
>>> breezedb.run_query("QUERY_HERE")

Alternatively, you may also want to store the query, or queries, in a variable for later use.

>>> import breezedb
>>> myquery = "QUERY1;;QUERY2;;QUERY3"
>>> breezedb.run_query(myquery)

.. _CREATE:

*****************
CREATE operations
*****************

The creation queries can be used to create **databases**, **tables**, **fields** and **element rows**.

Database creation
#################

The syntax for this operation is as follows::

    CREATE DB 'dbname' AT 'path'

This will create a new directory called *dbname* in the specified *path*

Table creation
##############

The syntax for this operation is as follows::

    CREATE TABLE 'table1' 'table2' 'table3' AT 'dbpath'

This will create tables in the database located in *dbpath*. Note that it is possible to include as many tables as desired.

Row creation
############

The syntax for this operation is as follows::

    CREATE ROW 'element1' 'element2' 'element3' IN 'table' AT 'dbpath'

This will create a new data row in the specified *table*. The number of element arguments **must be the number of fields present in the table**.

.. _GET:

**************
GET operations
**************

The get queries can be used to get the contents of **databases**, **tables**, **fields** and **elements**.

Database contents
#################

The syntax for this operation is as follows::

    GET TABLES AT 'dbpath'

This will return a list of tables present in the database at *dbpath*.

Table contents
##############

The syntax for this operation is as follows::

    GET FIELDS IN 'table' AT 'dbpath'

This will return a list of fields contained in the specified *table*.

Field types
###########

The syntax for this operation is as follows::

    GET TYPE OF 'field' IN 'table' AT 'dbpath'

This will return the *type* of the selected field. This is mainly used to know how to parse the elements of that field.

Field contents
##############

The syntax for this operation is as follows::

    GET ELEMENTS FROM 'field' IN 'table' AT 'dbpath'

This will return a list of element rows in the specified *field*.

Row contents
############

The syntax for this operation is as follows::

    GET ROW 'index' IN 'table' AT 'dbpath'

This will return the data row of the *table* in the position specified by *index*.

.. _REMOVE:

*****************
REMOVE operations
*****************

The removal queries can be used to remove the contents of **databases**, **tables**, **fields** and **elements**.

Database removal
################

The syntax for this operation is as follows::

    REMOVE DB AT 'dbpath'

This will delete the database located in *dbpath*.

Table removal
#############

The syntax for this operation is as follows::

    REMOVE TABLE 'table1' 'table2' 'table3' AT 'dbpath'

This will remove the specified tables in the database located in *dbpath*. Note that it is possible to include as many tables as desired.

Table removal
#############

The syntax for this operation is as follows::

    REMOVE FIELD 'field1' 'field2' 'field3' IN 'table' AT 'dbpath'

This will remove the specified fields in the *table*. Note that it is possible to include as many fields as desired.

Table removal
#############

The syntax for this operation is as follows::

    REMOVE ROW 'index1' 'index2' 'index3' IN 'table' AT 'dbpath'

This will remove the specified data rows in the *table*. Note that it is possible to include as many row indexes as desired.

.. _RENAME:

*****************
RENAME operations
*****************

The renaming queries can be used to rename **tables** and **fields**.

Table rename
############

The syntax for this operation is as follows::

    RENAME TABLE 'actual name' AT 'dbpath' TO 'new name'

This will substitute the name of the specified table to *new name*.

Field rename
############

The syntax for this operation is as follows::

   RENAME FIELD 'actual name' IN 'table' AT 'dbpath' TO 'new name'

This will substitute the name of the specified field to *new name*.

.. _EXISTS:

*****************
EXISTS operations
*****************

It is possible to check if a **table**, **field** or **element** exists in the database.

Table exists
############

The syntax for this operation is as follows::

    EXISTS TABLE 'table' AT 'dbpath'

This will determine whether the *table* exists in the database or not.

Field exists
############

The syntax for this operation is as follows::

    EXISTS FIELD 'field' IN 'table' AT 'dbpath'

This will determine whether the *field* exists in the *table* or not.

Element exists
##############

The syntax for this operation is as follows::

    EXISTS ELEMENT 'index' FROM 'field' IN 'table' AT 'dbpath'

This will determine whether the *element index* exists in the *field* or not.

.. _EMPTY:

****************
EMPTY operations
****************

It is possible to empty a **field** or **element** of the database.

Field emptying
##############

The syntax for this operation is as follows::

    EMPTY FIELD 'field1' 'field2' 'field3' IN 'table' AT 'dbpath'

This will empty the contents of the specified fields. Note that it is possible to include as many fields as desired.

Element emptying
################

The syntax for this operation is as follows::

    EMPTY ELEMENT 'index1' 'index2' 'index3' FROM 'field' IN 'table' AT 'dbpath'

This will empty the contents of the specified fields. Note that it is possible to include as many indexes as desired.

.. _FIND:

**************
FIND operation
**************

This operation is used to search for specific content in a given field::

    FIND 'content' FROM 'field' IN 'table' AT 'dbpath'

This will return the index matching the content searched.

.. _MODIFY:

****************
MODIFY operation
****************

This operation is used to modify the content of a specific element, instead of the complete data row, of a given field::

    MODIFY 'index' FROM 'field' IN 'table' AT 'dbpath' TO 'new content'

This will modify the content in the given index to *new content*.





