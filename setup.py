#!/usr/bin/env python
# '''
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.
# '''

import sys
import setuptools

deps = [
    "lxml",
    "numpy",
    "readability-lxml",
    "scikit-learn",
    "scipy",
    "urllib3"
]

setuptools.setup(
        name='tvnews',
        version='0.1.2',
        description='Recommends TV news clips related to given news articles',
        url='https://github.com/MaxReinisch/tvnews',
        author='Max W. Reinisch',
        author_email='reinischmax@gmail.com',
        long_description=open('README.md').read(),
        license='LICENSE.txt',
        packages=['tvnews'],
        install_requires=deps,
        test_suite='nose.collector',
        tests_require=['nose'],
        zip_safe=False,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha'
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries :: Python Modules',

        ])
