# -*- coding: utf-8 -*-

import doctest
import unittest


def test_suite():
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    globs= {}

    suite = unittest.TestSuite()
    for filename in ['bool.txt', 'choice.txt', 'collection.txt',
                     'multichoice.txt', 'object.txt', 'date.txt',
                     'radio.txt', 'uri.txt', 'time.txt']:
        test = doctest.DocFileSuite(
            filename,
            optionflags=optionflags,
            globs=globs)
        suite.addTest(test)

    return suite
