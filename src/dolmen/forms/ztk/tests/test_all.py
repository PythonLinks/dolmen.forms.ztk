# -*- coding: utf-8 -*-

import os.path
import cromlech.webob.request
import doctest
import dolmen.forms.ztk
import pkg_resources
import unittest
import webob.dec

from cromlech.io.interfaces import IPublicationRoot
from grokcore.component.testing import grok
from pkg_resources import resource_listdir
from zope.component import testing, provideAdapter, getMultiAdapter
from zope.component.testlayer import ZCMLFileLayer
from zope.i18n.interfaces.locales import ILocale
from zope.i18n.locales import locales
from zope.interface import Interface, directlyProvides
from zope.location import Location


class WSGIApplication(object):

    def __init__(self, context, formname):
        self.context = context
        self.formname = formname

    @webob.dec.wsgify(RequestClass=cromlech.webob.request.Request)
    def __call__(self, req):
        form = getMultiAdapter((self.context, req), Interface, self.formname)
        return form()


def get_locale(request):
    return locales.getLocale()


class TestLayer(ZCMLFileLayer):

    def setUp(self):
        ZCMLFileLayer.setUp(self)
        provideAdapter(get_locale, (Interface,), ILocale)

    def testSetUp(self):
        root = Location()
        directlyProvides(root, IPublicationRoot)
        self.root = root

    def makeApplication(self, context, formname):
        return WSGIApplication(context, formname)

    def getRootFolder(self):
        return self.root


layer = TestLayer(dolmen.forms.ztk)


def testsFromPackage(name):
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    files = pkg_resources.resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    globs = {'getRootFolder': layer.getRootFolder,
             'makeApplication': layer.makeApplication}

    for filename in files:

        if filename.endswith('_fixture.py'):
            continue

        if filename == '__init__.py':
            continue

        if filename.endswith('.py'):
            dottedname ='dolmen.forms.ztk.tests.%s.%s' % (name, filename[:-3])
            yield doctest.DocTestSuite(
                dottedname, optionflags=optionflags, globs=globs)
 
        elif filename.endswith('.txt'):
            yield doctest.DocFileSuite(
                os.path.join(name, filename),
                optionflags=optionflags, globs=globs)

 
def test_suite():
    suite = unittest.TestSuite()
    for folder in ['overview', 'widgets', 'integration']:
        for test in testsFromPackage(folder):
            suite.addTest(test)

    suite.layer = layer
    return suite
