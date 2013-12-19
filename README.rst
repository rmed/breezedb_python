breezedb
========

Source code is available in https://github.com/RMed/breezedb_python

Changelog
---------

- Added query parser
- Fixed some issues

A list of known issues is available here: https://github.com/RMed/breezedb_python/issues?state=open

**NOTE: version 1.1 will be the last version using XML structure and will be considered as *legacy*. Following versions of the library will not be backwards compatible.**

Overview
--------

- The database is organized in a file/directory way.
- Data is stored using *XML* structure.
- All database operations are done to the filesystem.
- It is not needed to distribute a database with your application, as it can be created on the go.

Installation
------------

- Linux/Unix (run with *superuser* permissions):

::

    # python setup.py install

or using pip::

    # pip install breezedb

- Windows (run as *administrator*):

::

    python.exe setup.py install

or using pip:

::

    python.exe pip install breezedb

or use the provided installer.

Documentation
-------------

Documentation is available online: http://pythonhosted.org/breezedb . This documentation includes all the available functions and extra information about the structure of the database and the query paraser.

If you want to build the documentation from source, navigate to the **doc** directory and run::

    make html

in Linux/Unix systems or::

    make.bat html

in Windows systems.

Test
----

There are several basic tests available in the **test** directory, you may want to check those out to get started.
