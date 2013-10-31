import unittest
import os, sys, shutil

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

database = os.path.join(test_root, 'db_temp')
table = 'users'

class TestField(unittest.TestCase):

    def test_field_exists_true(self):
        # Check for a field that does exist
        result = breezedb.field_exists('id', table, database)
        self.assertEqual(True, result)

    def test_field_exists_false(self):
        # Check for a field that does not exist
        result = breezedb.field_exists('test', table, database)
        self.assertEqual(False, result)

    def test_get_fieldtype(self):
        # Return the field type of 'id' (int)
        expected = 'int'
        result = breezedb.get_field_type('id', table, database)
        self.assertEqual(expected, result)

    def test_get_fieldtype_inexistent(self):
        # Attemp to get the field type of an inexistent field
        with self.assertRaises(breezedb.BreezeException):
            breezedb.get_field_type('test', table, database)

    def test_create_field(self):
        # Add a new field to the table
        breezedb.create_field('new_field', 'string', table, database)

    def test_create_field_existing(self):
        # Attempt to add an already existing field
        with self.assertRaises(breezedb.BreezeException):
            breezedb.create_field('new_field', 'string', table, database) 

    def test_remove_field(self):
        # Remove the previously created field
        breezedb.remove_field('new_field', table, database)

    def test_remove_field_inexistent(self):
        # Attempt to remove the field again
        with self.assertRaises(breezedb.BreezeException):
            breezedb.remove_field('new_field', table, database)

    def test_empty_field(self):
        # Empty the contents of the 'name' field
        breezedb.empty_field('name', table, database)

    def test_empty_field_inexistent(self):
        # Attempt to empty the contents of an inexistent field
        with self.assertRaises(breezedb.BreezeException):
            breezedb.empty_field('none', table, database)

    def test_get_element_list(self):
        # Get an element list from the 'last_name' field
        expected = ['McPerson1', 'McPerson2', 'McPerson3', 'McPerson4',
                    'McPerson5']
        result = breezedb.get_element_list('last_name', table, database)
        self.assertEqual(expected, result)

    def test_get_element_list_inexistent(self):
        # Attempt to get an element list from an inexistent field
        with self.assertRaises(breezedb.BreezeException):
            breezedb.get_element_list('test_field', table, database)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir(os.path.join(test_root, 'db_temp')):
        shutil.rmtree(os.path.join(test_root, 'db_temp'))
    # Create temp copy of the database
    shutil.copytree(os.path.join(test_root, 'db'),
        os.path.join(test_root, 'db_temp'))
    # Begin tests
    unittest.main()

