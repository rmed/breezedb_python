import unittest
import os, sys, shutil

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

import core as breeze

class TestDBOperations(unittest.TestCase):

    def test_create_breezedb(self):
        # Create a new database
        path = './'
        name = 'test_database1'
        breeze.db.create_breezedb(path, name)

    def test_create_breezedb_existing(self):
        # Try to create the database again
        with self.assertRaises(breeze.db.DBException):
            path = './'
            name = 'test_database1'
            breeze.db.create_breezedb(path, name)

    def test_remove_breezedb(self):
        # Remove previously created database
        path = 'test_database1'
        breeze.db.remove_breezedb(path)
        # Remove temp database
        temp = 'db_temp'
        breeze.db.remove_breezedb(temp)

    def test_remove_breezedb_inexistent(self):
        # Try to remove the databases again
        with self.assertRaises(breeze.db.DBException):
            path = 'test_database1'
            breeze.db.remove_breezedb(path)
            temp = 'db_temp'
            breeze.db.remove_breezedb(temp)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir('db_temp'):
        shutil.rmtree('db_temp')
    # Create temp copy of the database
    shutil.copytree('db', 'db_temp')
    # Begin tests
    unittest.main()

