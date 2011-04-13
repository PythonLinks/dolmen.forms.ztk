# -*- coding: utf-8 -*-

import unittest
import doctest
from grokcore.component.testing import grok


def setUp(test):
    grok('dolmen.forms.base')
    grok('dolmen.forms.ztk')


def test_suite():
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    globs= {}

    suite = unittest.TestSuite()
    for filename in ['fields.txt', 'validation.txt']:
        test = doctest.DocFileSuite(
            filename,
            setUp=setUp,
            optionflags=optionflags,
            globs=globs)
        suite.addTest(test)

    return suite
