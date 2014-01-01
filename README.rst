breezedb
========

Source code is available in https://github.com/RMed/breezedb_python
License: **GPLv2**

Changelog
---------

- New JSON structure
- Database now consists of a single file
- Improved special character support
- Improved exception handling
- Added several database operations

Issues and bug reports
----------------------

Please report any issues or bugs you may encounter in https://github.com/RMed/breezedb_python/issues

**NOTE: version 1.2.0 is not compatible with previous versions of the library.**

Overview
--------

- The data is contained within a single file using *JSON* structure.
- All database operations are done to the filesystem.
- Uses user session permissions for the database
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

Documentation is available online in http://pythonhosted.org/breezedb . This documentation includes all the available functions and extra information about the structure of the database and the query parser.

If you want to build the documentation from source, navigate to the **doc** directory and run::

    make html

in Linux/Unix systems or::

    make.bat html

in Windows systems.

Tests
-----

There are several basic tests available in the **test** directory that can be run after the library is installed.
