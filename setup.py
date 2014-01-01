# -*- coding: utf-8 -*-
#
# This file is part of breezedb - https://github.com/RMed/breezedb_python
#
# Copyright (C) 2013  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
# or see <http://www.gnu.org/licenses/>.

from distutils.core import setup

setup(
    name = 'breezedb',
    version = '1.2.0',
    description = 'A simple file-based database engine',
    author = 'Rafael Medina García',
    author_email = 'rafamedgar@gmail.com',
    url = 'https://github.com/RMed/breezedb_python',
    license = 'GPLv2',
    packages = ['breezedb'],
    package_dir = {'breezedb': 'breezedb'},

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )
