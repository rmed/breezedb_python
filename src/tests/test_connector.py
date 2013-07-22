# -*-# -*- coding: utf-8 -*-
# This file is part of BreezeDB - https://github.com/RMed/breeze_db
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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

if __name__ == "__main__":
    # Remove previous temp copy
    if os.path.isdir('db_temp'):
        shutil.rmtree('db_temp')
    # Create temp copy of the database
    shutil.copytree('db', 'db_temp')
    # Begin tests
    unittest.main()
