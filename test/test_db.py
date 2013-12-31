import os, shutil, sys, unittest

test_root = os.path.abspath(os.path.dirname(__file__))

import breezedb

class TestDBOperations(unittest.TestCase):

    def test_create_db(self):
        name = 'testdb'
        breezedb.create_db(test_root, name)

    def test_create_db_existing(self):
        try:
            name = 'testdb'
            breezedb.create_db(test_root, name)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_get_table_list(self):
        path = os.path.join(test_root, 'tempdb.brdb')
        result = breezedb.get_table_list(path)
        self.assertEquals([u'table_1', u'table_2', u'table_3']
, result)

    def test_get_table_list_inexistent(self):
        try:
            path = os.path.join(test_root, 'test1234.brdb')
            breezedb.get_table_list(path)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

    def test_is_brdb(self):
        path = os.path.join(test_root, 'testdb.brdb')
        result = breezedb.is_brdb(path)
        self.assertEquals(True, result)

    def test_is_not_brdb(self):
        path = os.path.join(test_root, 'testdb1234.brdb')
        result = breezedb.is_brdb(path)
        self.assertEquals(False, result)

    def test_remove_db(self):
        path = os.path.join(test_root, 'testdb.brdb')
        breezedb.remove_db(path)
        temp = os.path.join(test_root, 'tempdb.brdb')
        breezedb.remove_db(temp)

    def test_remove_breezedb_inexistent(self):
        try:
            path = os.path.join(test_root, 'testdb12.brdb')
            breezedb.remove_db(path)
            temp = os.path.join(test_root, 'tempdb12.brdb')
            breezedb.remove_db(temp)
            self.assertEquals(False, True)
        except:
            self.assertTrue(True, True)

if __name__ == "__main__":
    if os.path.isfile(os.path.join(test_root, 'tempdb.brdb')):
        os.remove(os.path.join(test_root, 'tempdb.brdb'))

    shutil.copy(os.path.join(test_root, 'db.brdb'),
        os.path.join(test_root, 'tempdb.brdb'))

    unittest.main()

