import os, sys, shutil, unittest

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

db = os.path.join(test_root, 'dbtemp.brdb')
table = 'table_1'

class TestElement(unittest.TestCase):

    def test_create_row(self):
        breezedb.create_row([0, 'new Name', 'new Name2'], table, db)

    def test_create_row_invalid_length(self):
        try:
            breezedb.create_row([0, 'new Name'], table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_empty_element(self):
        breezedb.empty_element(0, 'id', table, db)

    def test_empty_element_inexistent(self):
        try:
            breezedb.empty_element(10, 'id', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_exists_row_true(self):
        result = breezedb.exists_row(0, table, db)
        self.assertEquals(result, True)

    def test_exists_row_false(self):
        result = breezedb.exists_row(11, table, db)
        self.assertEquals(result, False)

    def test_get_element_data(self):
        result = breezedb.get_element_data(0, 'name', table, db)
        self.assertEquals(result, u'Name1')

    def test_get_element_data_inexistent(self):
        try:
            result = breezedb.get_element_data(100, 'name', table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_modify_element(self):
        breezedb.modify_element(0, 'id', table, db, 13)

    def test_modify_element_inexistent(self):
        try:
            breezedb.modify_element(110, 'id', table, db, 13)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_remove_row(self):
        breezedb.remove_row(0, table, db)

    def test_remove_row_inexistent(self):
        try:
            breezedb.remove_row(110, table, db)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

if __name__ == "__main__":
    if os.path.isfile(os.path.join(test_root, 'dbtemp.brdb')):
        os.remove(os.path.join(test_root, 'dbtemp.brdb'))

    shutil.copy(os.path.join(test_root, 'db.brdb'),
        os.path.join(test_root, 'dbtemp.brdb'))

    unittest.main()

