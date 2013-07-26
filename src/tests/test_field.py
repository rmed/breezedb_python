import unittest
import os, sys, shutil

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

from operations import field as fieldops

database = 'db_temp'
table = 'users'

class TestField(unittest.TestCase):

    def test_field_exists_true(self):
        # Check for a field that does exist
        result = fieldops.field_exists('id', table, database)
        self.assertEqual(True, result)

    def test_field_exists_false(self):
        # Check for a field that does not exist
        result = fieldops.field_exists('test', table, database)
        self.assertEqual(False, result)

    def test_get_fieldtype(self):
        # Return the field type of 'id' (int)
        expected = 'int'
        result = fieldops.get_fieldtype('id', table, database)
        self.assertEqual(expected, result)

    def test_get_fieldtype_inexistent(self):
        # Attemp to get the field type of an inexistent field
        with self.assertRaises(fieldops.FieldException):
            fieldops.get_fieldtype('test', table, database)

    def test_add_field(self):
        # Add a new field to the table
        fieldops.add_field('new_field', 'string', table, database)

    def test_add_field_existing(self):
        # Attempt to add an already existing field
        with self.assertRaises(fieldops.FieldException):
            fieldops.add_field('new_field', 'string', table, database) 

    def test_remove_field(self):
        # Remove the previously created field
        fieldops.remove_field('new_field', table, database)

    def test_remove_field_inexistent(self):
        # Attempt to remove the field again
        with self.assertRaises(fieldops.FieldException):
            fieldops.remove_field('new_field', table, database)

    def test_empty_field(self):
        # Empty the contents of the 'name' field
        fieldops.empty_field('name', table, database)

    def test_empty_field_inexistent(self):
        # Attempt to empty the contents of an inexistent field
        with self.assertRaises(fieldops.FieldException):
            fieldops.empty_field('none', table, database)

    def test_get_element_list(self):
        # Get an element list from the 'last_name' field
        expected = ['McPerson1', 'McPerson2', 'McPerson3', 'McPerson4',
                    'McPerson5']
        result = fieldops.get_elementlist('last_name', table, database)
        self.assertEqual(expected, result)

    def test_get_element_list_inexistent(self):
        # Attempt to get an element list from an inexistent field
        with self.assertRaises(fieldops.FieldException):
            fieldops.get_elementlist('test_field', table, database)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir('db_temp'):
        shutil.rmtree('db_temp')
    # Create temp copy of the database
    shutil.copytree('db', 'db_temp')
    # Begin tests
    unittest.main()

