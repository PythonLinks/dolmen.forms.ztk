# -*- coding: utf-8 -*-

import crom
import doctest
import dolmen.forms.base
import dolmen.forms.ztk
import os.path
import pkg_resources
import unittest
import webob.dec

from crom import testing
from cromlech.webob.request import Request
from cromlech.browser.interfaces import IPublicationRoot
from dolmen.collection import load
from dolmen.forms.ztk.fields import registerDefault
from pkg_resources import resource_listdir
from zope.interface import Interface, directlyProvides
from zope.location import Location


def setUp(test):
    testing.setup()
    registerDefault()
    load.reloadComponents()
    crom.configure(dolmen.forms.base)
    crom.configure(dolmen.forms.ztk)


def tearDown(test):
    testing.teardown()


class WSGIApplication(object):

    def __init__(self, context, formname):
    	self.context = context
        self.formname = formname

    @webob.dec.wsgify(RequestClass=Request)
    def __call__(self, req):
        form = Interface(self.context, req, name=self.formname)
        return form()


def testsFromPackage(name):
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    files = pkg_resources.resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    globs = {'makeApplication': WSGIApplication}

    for filename in files:

        if filename.endswith('_fixture.py'):
            continue

        if filename == '__init__.py':
            continue

        if filename.endswith('.py'):
            dottedname ='dolmen.forms.ztk.tests.%s.%s' % (name, filename[:-3])
            yield doctest.DocTestSuite(
                dottedname,
                optionflags=optionflags,
                setUp=setUp,
                tearDown=tearDown,
                globs=globs)

        elif filename.endswith('.txt'):
            yield doctest.DocFileSuite(
                os.path.join(name, filename),
                optionflags=optionflags,
                setUp=setUp,
                tearDown=tearDown,
                globs=globs)


def test_suite():
    suite = unittest.TestSuite()
    for folder in ['overview', 'widgets', 'integration']:
        for test in testsFromPackage(folder):
            suite.addTest(test)
    return suite
