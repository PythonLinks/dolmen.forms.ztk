# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '0.1dev'

tests_require = [
    'WebOb',
    'cromlech.webob',
    'dolmen.location',
    'infrae.testbrowser',
    'zope.configuration',
    'zope.location',
    'zope.security',
    ]

setup(name='dolmen.forms.ztk',
      version=version,
      description="Zope Toolkit support for dolmen.forms",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zeam form zope schema edit content',
      author='Sylvain Viollon',
      author_email='thefunny@gmail.com',
      url='http://pypi.python.org/pypi/dolmen.forms.ztk',
      license='BSD',
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.forms'],
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'cromlech.browser',
          'cromlech.io',
          'dolmen.forms.base',
          'dolmen.template',
          'grokcore.component',
          'setuptools',
          'zope.component',
          'zope.event',
          'zope.i18n',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.schema',
        ],
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      [dolmen.collection.components]
      default = dolmen.forms.ztk.fields:registerDefault
      bool = dolmen.forms.ztk.widgets.bool:register
      choice = dolmen.forms.ztk.widgets.choice:register
      collection = dolmen.forms.ztk.widgets.collection:register
      date = dolmen.forms.ztk.widgets.date:register
      number = dolmen.forms.ztk.widgets.number:register
      object = dolmen.forms.ztk.widgets.object:register
      password = dolmen.forms.ztk.widgets.password:register
      text = dolmen.forms.ztk.widgets.text:register
      textline = dolmen.forms.ztk.widgets.textline:register
      uri = dolmen.forms.ztk.widgets.uri:register
      time = dolmen.forms.ztk.widgets.time:register
      """,
      )
