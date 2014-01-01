breezedb
========

A simple file-based database engine.

**This repository contains the *Python* implementation of breezedb. Documentation is available from source or [online](http://pythonhosted.org/breezedb)**

This code is written for **Python 2.7**

Licensed under [GPLv2](http://www.gnu.org/licenses/gpl-2.0.html)

## Main features

- breezedb aims to be a simple way of storing data in files, avoiding the need for a database server to be installed and running in the machine.
- Stores data in a *single file*
- It is meant to store small amounts of data.
- All operations are done on the local file system.
- There is no need to redistribute a database with your application, as it can be created on the go.
- *JSON* structure for organizing the data.

## Installation

You can install the library from source by running:

```
python setup.py install
```

with the required permissions. You can also install it from PyPI by running:

```
pip install breezedb
```

---

For more information, including structures and organization, please [visit the documentation](http://pythonhosted.org/breezedb).
