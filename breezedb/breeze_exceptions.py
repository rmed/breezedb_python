# -*- coding: utf-8 -*-
#
# This file is part of breezedb - https://github.com/RMed/breezedb_python
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
.. module:: exceptions
    :platform: Unix, Windows
    :synopsis: BreezeDB exception handler.

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

import sys

class BreezeException(Exception):
    """ This exception is raised by the modules if a regular exception
        occurs.

        :arg str level: library level in which the exception occured 
             (db, table, field or element)
        :arg str message: information message to print
    """

    def __init__(self, level, message):
        self.level = level
        self.message = message
        self.exception_message()

    def exception_message(self):
        """ This function simply writes a message into the stderr indicating
            why (and where) the exception was produced.
        """
        sys.stderr.write('Exception in %s: %s' % (self.level, self.message))

