import unittest
import os, sys, shutil

sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]

from connector import Connector

# Create test connector
connector_tester = Connector('db_temp')

class TestConnector(unittest.TestCase):

    def test_get_tablelist(self):
        expected = ['cities', 'languages', 'users']
        result = connector_tester.get_tablelist()
        self.assertEqual(expected, result)

import connector

class TestDBOperations(unittest.TestCase):

    def test_create_breezedb(self):
        # Create a new database
        path = './'
        name = 'test_database1'
        connector.create_breezedb(path, name)

    def test_create_breezedb_existing(self):
        # Try to create the database again
        with self.assertRaises(connector.ConnectorException):
            path = './'
            name = 'test_database1'
            connector.create_breezedb(path, name)

    def test_remove_breezedb(self):
        # Remove previously created database
        path = 'test_database1'
        connector.remove_breezedb(path)
        # Remove temp database
        temp = 'db_temp'
        connector.remove_breezedb(temp)

    def test_remove_breezedb_inexistent(self):
        # Try to remove the databases again
        with self.assertRaises(connector.ConnectorException):
            path = 'test_database1'
            connector.remove_breezedb(path)
            temp = 'db_temp'
            connector.remove_breezedb(temp)

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir('db_temp'):
        shutil.rmtree('db_temp')
    # Create temp copy of the database
    shutil.copytree('db', 'db_temp')
    # Begin tests
    unittest.main()

