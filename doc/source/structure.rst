Database Structure
==================

********
Overview
********

breezedb makes use of **files and directories** in order to create a database, organizing the data in tables and fields:

- **Tables**: Subdirectories of the root of the database that contain differet fields and a special file that specifies the order of those fields.
- **Fields**: Files *without* extension whose contents are organized using *XML* structure. The type of the data that a field contains is specified at the beginning of the file.

There are also two **special files** located in the root of the database and in each table, respectively:

- root.breeze_: This file sets the root of the database and contains all the different tables.
- tableinfo.breeze_: This file specifies the fields that are contained in a table.

An example structure would be as follows::

    /
    root.breeze
    example_table_1/
        tableinfo.breeze
        id
        name
        location
    example_table_2/
        tableinfo.breeze
        day
        month
        year

.. _root.breeze:

**************
Root structure
**************

The root of the database is set at the locaton of the **root.breeze** file. This is the only file located in the root directory (apart from the table subdirectories)

The **root.breeze** file contains an **alphabetically ordered list** of all the subdirectories (tables) included in the database with an XML structure::

    <breeze>
        <table>table_example_names</table>
        <table>table_example_options</table>
        <table>table_id</table>
        <table>table_post</table>
    </breeze>

.. _tableinfo.breeze:

***************
Table structure
***************

Tables are unique *subdirectories* that contain the *field* files. A table **cannot contain another table**. In each table, there is a **tableinfo.breeze** file that contains an ordered list (by priority) of the fields contained in the table. Each field is represented as a file named after the field without extension.

The **tableinfo.breeze** file has an XML structure and its contents are ordered by priority, meaning that the first element will have the highest priority and the last element the lowest::

    <breeze>
        <field>id</field>
        <field>name</field>
        <field>location</field>
        <field>number</field>
    </breeze>

The example above would result in a structure similar to this:

====  ========  ========  =========
 id     name    location  number
====  ========  ========  =========
234   Person 1  Paris     123456789
5371  Person 2  London    248795641
4687  Person 3  Berlin    875469853
====  ========  ========  =========


***************
Field structure
***************

A field is a type of data contained in a table. Each field is represented by a file without extension and the data is stored using an XML structure. All the fields in a table are synced in such a way that when an element is removed from the table, all the fields must delete their corresponding element (identified by an index) and update the indexes of the remaining elements. The type of data contained in a field is specified at the beginning of the file.

This is an example of a field structure::

    <breeze>
        <type>string</type>
        <element index="0">Element 1</element>
        <element index="1">Element 2</element>
        <element index="2">Test element 3</element>
        <element index="3">Another test element</element>
    </breeze>

Data types
##########

Virtually, Breeze stores the data in a text file, but there is no real limitation regarding what can be stored in the database, as long as the specific programming language can treat the data accordingly. In order to have a better portability of the code, we can specify the following simple data types:

- *string*: For storing any kind of text, including single characters.

- *int*: For storing integer numbers.

- *double/float*: For storing real numbers (with double precision).

- *boolean*: For storing true/false statements. The boolean type is **treated as a single bit** (int) for a simpler approach. Therefore::

    0 => false
    1 => true

