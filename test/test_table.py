import os, shutil, sys, unittest

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

db = os.path.join(test_root, 'dbtemp.brdb')

class TestTable(unittest.TestCase):

    def test_create_table(self):
        breezedb.create_table('new_table', db)

    def test_create_table_existing(self):
        try:
            breezedb.create_table('new_table', db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_exists_table_true(self):
        result = breezedb.exists_table('table_1', db)
        self.assertEqual(True, result)

    def test_exists_table_false(self):
        result = breezedb.exists_table('test', db)
        self.assertEqual(False, result)

    def test_get_row(self):
        result = breezedb.get_row(0, 'table_1', db)
        self.assertEqual([0, u'Name1', u'Name2'], result)

    def test_get_row_inexistent(self):
        try:
            result = breezedb.get_row(10, 'table_1', db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_get_field_list(self):
        result = breezedb.get_field_list('table_1', db)
        self.assertEqual([u'id', u'name', u'name2'], result)

    def test_get_field_list_inexistent(self):
        try:
            result = breezedb.get_field_list('table_1123', db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_rename_table(self):
        breezedb.rename_table('table_2', db, 'table_21')

    def test_rename_table_inexistent(self):
        try:
            breezedb.rename_table('table_2', db, 'table_21')
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_remove_table(self):
        breezedb.remove_table('table_3', db)

    def test_remove_table_inexistent(self):
        try:
            breezedb.remove_table('table_3', db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_search_data(self):
        expected = [0, 1]
        result = breezedb.search_data('name1', 'table_1', db)
        self.assertEquals(expected, result)

if __name__ == "__main__":
    if os.path.isfile(os.path.join(test_root, 'dbtemp.brdb')):
        os.remove(os.path.join(test_root, 'dbtemp.brdb'))

    shutil.copy(os.path.join(test_root, 'db.brdb'),
        os.path.join(test_root, 'dbtemp.brdb'))

    unittest.main()

