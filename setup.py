#!/usr/bin/env python
#This file is part stock_origin module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from setuptools import setup
import re

info = eval(open('__tryton__.py').read())
major_version, minor_version, _ = info.get('version', '0.0.1').split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res|webdav)(\W|$)', dep):
        requires.append('trytond_%s >= %s.%s, < %s.%s' %
                (dep, major_version, minor_version, major_version,
                    minor_version + 1))
requires.append('trytond >= %s.%s, < %s.%s' %
        (major_version, minor_version, major_version, minor_version + 1))

setup(name='trytond_stock_origin',
    version=info.get('version', '0.0.1'),
    description=info.get('description', ''),
    author=info.get('author', 'Zikzakmedia'),
    author_email=info.get('email', 'zikzak@zikzakmedia.com'),
    url=info.get('website', 'http://www.zikzakmedia.com'),
    download_url="https://bitbucket.org/zikzakmedia/trytond-stock_origin",
    package_dir={'trytond.modules.stock_origin': '.'},
    packages=[
        'trytond.modules.stock_origin',
        'trytond.modules.stock_origin.tests',
    ],
    package_data={
        'trytond.modules.stock_origin': info.get('xml', []) \
                + info.get('translation', []),
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Catalan',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business',
    ],
    license='GPL-3',
    install_requires=requires,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    stock_origin = trytond.modules.stock_origin
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
)
