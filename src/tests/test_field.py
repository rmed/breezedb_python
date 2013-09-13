import unittest
import os, sys, shutil

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

import breezedb.core as breeze 

database = 'db_temp'
table = 'users'

class TestField(unittest.TestCase):

    def test_field_exists_true(self):
        # Check for a field that does exist
        result = breeze.field.exists('id', table, database)
        self.assertEqual(True, result)

    def test_field_exists_false(self):
        # Check for a field that does not exist
        result = breeze.field.exists('test', table, database)
        self.assertEqual(False, result)

    def test_get_fieldtype(self):
        # Return the field type of 'id' (int)
        expected = 'int'
        result = breeze.field.get_type('id', table, database)
        self.assertEqual(expected, result)

    def test_get_fieldtype_inexistent(self):
        # Attemp to get the field type of an inexistent field
        with self.assertRaises(breeze.field.FieldException):
            breeze.field.get_type('test', table, database)

    def test_add_field(self):
        # Add a new field to the table
        breeze.field.add('new_field', 'string', table, database)

    def test_add_field_existing(self):
        # Attempt to add an already existing field
        with self.assertRaises(breeze.field.FieldException):
            breeze.field.add('new_field', 'string', table, database) 

    def test_remove_field(self):
        # Remove the previously created field
        breeze.field.remove('new_field', table, database)

    def test_remove_field_inexistent(self):
        # Attempt to remove the field again
        with self.assertRaises(breeze.field.FieldException):
            breeze.field.remove('new_field', table, database)

    def test_empty_field(self):
        # Empty the contents of the 'name' field
        breeze.field.empty('name', table, database)

    def test_empty_field_inexistent(self):
        # Attempt to empty the contents of an inexistent field
        with self.assertRaises(breeze.field.FieldException):
            breeze.field.empty('none', table, database)

    def test_get_element_list(self):
        # Get an element list from the 'last_name' field
        expected = ['McPerson1', 'McPerson2', 'McPerson3', 'McPerson4',
                    'McPerson5']
        result = breeze.field.get_elementlist('last_name', table, database)
        self.assertEqual(expected, result)

    def test_get_element_list_inexistent(self):
        # Attempt to get an element list from an inexistent field
        with self.assertRaises(breeze.field.FieldException):
            breeze.field.get_elementlist('test_field', table, database)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir('db_temp'):
        shutil.rmtree('db_temp')
    # Create temp copy of the database
    shutil.copytree('db', 'db_temp')
    # Begin tests
    unittest.main()

