import unittest
import os, sys, shutil

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

import core as breeze

database = 'db_temp'

class TestTable(unittest.TestCase):

    def test_table_exists_true(self):
        # Check for a table that does exist
        result = breeze.table.table_exists('cities', database)
        self.assertEqual(True, result)

    def test_table_exists_false(self):
        # Check for a table that does not exist
        result = breeze.table.table_exists('test', database)
        self.assertEqual(False, result)

    def test_add_table(self):
        # Add a new table to the database
        breeze.table.add_table('new_table', database)

    def test_remove_table_exists(self):
        # Remove the previously created table
        breeze.table.remove_table('new_table', database)

    def test_remove_table_inexistent(self):
        # Try to remove the previously created table again
        with self.assertRaises(breeze.table.TableException):
            breeze.table.remove_table('new_table', database)

    def test_get_fieldlist(self):
        # Get a list of fields from table 'languages'
        expected = ['name', 'cross_platform']
        result = breeze.table.get_fieldlist('languages', database)
        self.assertEqual(expected, result)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir('db_temp'):
        shutil.rmtree('db_temp')
    # Create temp copy of the database
    shutil.copytree('db', 'db_temp')
    # Begin tests
    unittest.main()

