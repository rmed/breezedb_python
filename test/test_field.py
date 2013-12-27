import os, sys, shutil, unittest

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

db = os.path.join(test_root, 'dbtemp.brdb')
table = 'table_1'

class TestField(unittest.TestCase):

    def test_create_field(self):
        breezedb.create_field('new_field', 'str', table, db)

    def test_create_field_existing(self):
        try:
            breezedb.create_field('new_field', 'str', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_empty_field_row(self):
        breezedb.empty_field_row(0, 'id', table, db)

    def test_empty_field_row_inexistent(self):
        try:
            breezedb.empty_field_row(0, 'id123', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_empty_field_table(self):
        breezedb.empty_field_table('name', table, db)

    def test_empty_field_table_inexistent(self):
        try:
            breezedb.empty_field_table('name1234', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_exists_field_true(self):
        result = breezedb.exists_field('id', table, db)
        self.assertEquals(result, True)

    def test_exists_field_false(self):
        result = breezedb.exists_field('id1234', table, db)
        self.assertEquals(result, False)

    def test_get_field_data(self):
        result = breezedb.get_field_data('name2', table, db)
        self.assertEquals([u'Name2', u'Name21'], result)

    def test_get_field_data_inexistent(self):
        try:
            breezedb.get_field_data('name223', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_get_field_type(self):
        result = breezedb.get_field_type('name2', table, db)
        self.assertEquals(u'str', result)

    def test_rename_field(self):
        breezedb.rename_field('name2', table, db, 'name3')

    def test_rename_field_inexistent(self):
        try:
            breezedb.rename_field('name2', table, db, 'name3')
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_remove_field(self):
        breezedb.remove_field('id', table, db)

    def test_remove_field_inexistent(self):
        try:
            breezedb.remove_field('id', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_swap_fields(self):
        breezedb.swap_fields(0, 1, table, db)

    def test_swap_fields_inexistent(self):
        try:
            breezedb.swap_fields(10, 1, table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

if __name__ == "__main__":
    if os.path.isfile(os.path.join(test_root, 'dbtemp.brdb')):
        os.remove(os.path.join(test_root, 'dbtemp.brdb'))

    shutil.copy(os.path.join(test_root, 'db.brdb'),
        os.path.join(test_root, 'dbtemp.brdb'))

    unittest.main()

