breezedb
========

Characteristics
---------------

- The database is organized in a file/directory way.
- Data is stored using *XML* structure.
- All database operations are done to the filesystem.
- It is not needed to distribute a database with your application, as it can be created on the go.

Installation
------------

- Linux/Unix (run with *superuser* permissions)

::

    # python setup.py install

or using pip

::

    # pip install breezedb

- Windows (run as *administrator*)

::

    python.exe setup.py install

or using pip

::

    python.exe pip install breezedb

or use the provided installer.

Documentation
-------------

Documentation is available online at PyPI. If you want to build the documentation from source, navigate to the **doc** directory and run:

::

    make html

For Linux/Unix systems or

::

    make.bat html

For Windows systems.

Test
----

There are several basic tests available in the **test** directory, you may want to check those out to get started.
