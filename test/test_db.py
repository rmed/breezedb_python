import unittest
import os, sys, shutil

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

class TestDBOperations(unittest.TestCase):

    def test_create_breezedb(self):
        # Create a new database
        path = test_root
        name = 'test_database1'
        breezedb.create_db(path, name)

    def test_create_breezedb_existing(self):
        # Try to create the database again
        with self.assertRaises(breezedb.BreezeException):
            path = test_root
            name = 'test_database1'
            breezedb.create_db(path, name)

    def test_remove_breezedb(self):
        # Remove previously created database
        path = os.path.join(test_root,'test_database1')
        breezedb.remove_db(path)
        # Remove temp database
        temp = os.path.join(test_root,'db_temp')
        breezedb.remove_db(temp)

    def test_remove_breezedb_inexistent(self):
        # Try to remove the databases again
        with self.assertRaises(breezedb.BreezeException):
            path = 'test_database1'
            breezedb.remove_db(path)
            temp = 'db_temp'
            breezedb.remove_db(temp)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir(os.path.join(test_root, 'db_temp')):
        shutil.rmtree(os.path.join(test_root, 'db_temp'))
    # Create temp copy of the database
    shutil.copytree(os.path.join(test_root, 'db'),
        os.path.join(test_root, 'db_temp'))
    # Begin tests
    unittest.main()

