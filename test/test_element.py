import unittest
import os, sys, shutil

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

database = os.path.join(test_root, 'db_temp')
table = 'cities'
field = 'name'

class TestElement(unittest.TestCase):

    def test_element_exists_true(self):
        # Check for an element that does exist
        result = breezedb.element_exists(2, field, table, database)
        self.assertEqual(True, result)

    def test_element_exists_false(self):
        # Check for an element that does not exist
        result = breezedb.element_exists(10, field, table, database)
        self.assertEqual(False, result)
        
    def test_get_element_content(self):
        # Get the data of element located in position 1
        expected = 'Paris'
        result = breezedb.get_element_content(1, field, table, database)
        self.assertEqual(expected, result)

    def test_get_element_content_inexistent(self):
        # Attempt to get the data of an inexistent element
        with self.assertRaises(breezedb.BreezeException):
            breezedb.get_element_content(10, field, table, database)

    def test_find_element(self):
        # Find the index for 'Madrid'
        expected = 3
        result = breezedb.find_element('Madrid', field, table, database)
        # Must treat the result as integer
        self.assertEqual(expected, int(result[0]))

    def test_find_element_inexistent(self):
        # Attempt to find 'Tokyo'
        expected = []
        result = breezedb.find_element('Tokyo', field, table, database)
        # Must return an empty array
        self.assertEqual(expected, result)

    def test_modify_element(self):
        # Modify the last element
        breezedb.modify_element(4, 'Nowhere', field, table, database)

    def test_modify_element_inexistent(self):
        # Modify the last element
        with self.assertRaises(breezedb.BreezeException):
            breezedb.modify_element(35, 'Test Name', field, table, database)

    def test_empty_element(self):
        # Empty the content of element 0
        breezedb.empty_element(0, field, table, database)

    def test_empty_element_inexistent(self):
        # Attempt to empty the content of an inexistent element
        with self.assertRaises(breezedb.BreezeException):
            breezedb.empty_element(10, field, table, database)

    def test_remove_row(self):
        # Remove the complete row in position 2
        breezedb.remove_element_row(2, table, database)

    def test_remove_row_inexistent(self):
        # Attemptto remove an inexistent row
        with self.assertRaises(breezedb.BreezeException):
            breezedb.remove_element_row(100, table, database)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir(os.path.join(test_root, 'db_temp')):
        shutil.rmtree(os.path.join(test_root, 'db_temp'))
    # Create temp copy of the database
    shutil.copytree(os.path.join(test_root, 'db'),
        os.path.join(test_root, 'db_temp'))
    # Begin tests
    unittest.main()

