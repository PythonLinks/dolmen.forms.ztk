# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '2.4-dev'
readme = open("README.txt").read()
history = open(os.path.join("docs", "HISTORY.txt")).read()

install_requires=[
    'cromlech.browser >= 0.4',
    'dolmen.forms.base >= 2.2.4',
    'dolmen.location',
    'dolmen.template',
    'dolmen.clockwork',
    'grokcore.component',
    'setuptools',
    'zope.component',
    'zope.i18n',
    'zope.interface',
    'zope.schema',
    'fanstatic',
    'zeam.jsontemplate',
    ],

tests_require = [
    'WebOb',
    'cromlech.browser [test]',
    'cromlech.webob',
    'infrae.testbrowser',
    'zope.configuration',
    'zope.location',
    ]

setup(name='dolmen.forms.ztk',
      version=version,
      description="Zope Toolkit support for dolmen.forms",
      long_description="%s\n\n%s" % (readme, history),
      classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Cromlech Dolmen Form Zope',
      author='The Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://pypi.python.org/pypi/dolmen.forms.ztk',
      license='BSD',
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.forms'],
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      tests_require = tests_require,
      install_requires = install_requires,
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

      [fanstatic.libraries]
      dolmen_forms_ztk = dolmen.forms.ztk.resources:DolmenFormsZTKLibrary
      """,
      )
