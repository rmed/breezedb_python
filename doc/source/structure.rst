Database Structure
==================

********
Overview
********

breezedb makes use of a single **file** in order to create a database, organizing the data in tables and fields:

- **Tables**: Contain different fields and data rows.
- **Fields**: Specify the data that is stored in a specific position of the data row and the data type it contains.

This file is stored using a JSON structure. An example of this would be::

    {
        "table_1": {
            "fields": [
                {
                    "id": "int"
                }, 
                {
                    "name": "str"
                }, 
                {
                    "name2": "str"
                }
            ], 
            "rows": [
                {
                    "id": 0, 
                    "name": "Name1", 
                    "name2": "Name2"
                }, 
                {
                    "id": 23, 
                    "name": "Name12", 
                    "name2": "Name21"
                }
            ]
        }
    }

The root of the database is a simple dictionary. The keys added to this dictionary are tables and there cannot be two tables with the same name.

***************
Table structure
***************

Tables have two different keys: **fields** and **rows**:

- **fields**: contains the fields available for storing data. The order of the keys here is the priority in which they should be parsed.
- **rows**: rows are simply formed by the set of fields of the table. Each field position of the row stores a different type of data.

For example::

    "table_1": {
        "fields": [
            {
                "id": "int"
            },
            {
                "name": "str"
            },
            {
                "location": "str"
            },
            {
                "number": "int"
            }
        ],
        "rows": [
            {
                "id": 234,
                "location": "Paris",
                "name": "Person 1",
                "number": 123456789
            },
            {
                "id": 5371,
                "location": "248795641",
                "name": "Person 2",
                "number": 123456789
            },
            {
                "id": 234,
                "location": "Berlin",
                "name": "Person 3",
                "number": 875469853
            }
        ]
    }

Would result in a structure similar to this:

====  ========  ========  =========
 id     name    location  number
====  ========  ========  =========
234   Person 1  Paris     123456789
5371  Person 2  London    248795641
4687  Person 3  Berlin    875469853
====  ========  ========  =========

Data types
##########

The available data types are:

- *str*: For storing any kind of text, including single characters.

- *int*: For storing integer numbers.

- *float*: For storing real numbers (with double precision).

- *bool*: For storing true/false statements. The boolean type is **treated as a single bit** (int) for a simpler approach. Therefore::

    0 => false
    1 => true

