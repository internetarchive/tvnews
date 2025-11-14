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

import setuptools


setuptools.setup(
        name='tvnews',
        version='0.2.6',
        description='Recommends TV news clips related to given news articles',
        url='https://github.com/internetarchive/tvnews',
        author='Max W. Reinisch',
        author_email='reinischmax@gmail.com',
        long_description=open('README.md').read(),
        license='LICENSE.txt',
        packages=['tvnews'],
        install_requires=[
            "readability-lxml>=0.8.1",
            "scikit-learn",
            "scipy",
            "numpy<2",
            "spacy==3.7.5",
            "urllib3==2.5.0",
            "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz"
        ],
        tests_require=[
            'pytest',
            'pytest-xdist',
            'mock'
            ],
        zip_safe=False,
        classifiers=[
            'Development Status :: 4 - Beta'
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ])
