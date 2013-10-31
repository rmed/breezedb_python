import unittest
import os, sys, shutil

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

database = os.path.join(test_root, 'db_temp')

class TestTable(unittest.TestCase):

    def test_table_exists_true(self):
        # Check for a table that does exist
        result = breezedb.table_exists('cities', database)
        self.assertEqual(True, result)

    def test_table_exists_false(self):
        # Check for a table that does not exist
        result = breezedb.table_exists('test', database)
        self.assertEqual(False, result)

    def test_add_table(self):
        # Add a new table to the database
        breezedb.create_table('new_table', database)

    def test_remove_table_exists(self):
        # Remove the previously created table
        breezedb.remove_table('new_table', database)

    def test_remove_table_inexistent(self):
        # Try to remove the previously created table again
        with self.assertRaises(breezedb.BreezeException):
            breezedb.remove_table('new_table', database)

    def test_get_field_list(self):
        # Get a list of fields from table 'languages'
        expected = ['name', 'cross_platform']
        result = breezedb.get_field_list('languages', database)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir(os.path.join(test_root, 'db_temp')):
        shutil.rmtree(os.path.join(test_root, 'db_temp'))
    # Create temp copy of the database
    shutil.copytree(os.path.join(test_root, 'db'),
        os.path.join(test_root, 'db_temp'))
    # Begin tests
    unittest.main()

