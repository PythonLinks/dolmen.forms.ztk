# -*- coding: utf-8 -*-

import pytest
import crom
import dolmen.forms.base
import dolmen.forms.ztk
import webob.dec

from crom import testing
from cromlech.webob.request import Request
from dolmen.collection import load
from dolmen.forms.ztk.fields import registerDefault
from zope.interface import Interface


def crom_setup():
    testing.setup()
    registerDefault()
    load.reloadComponents()
    crom.configure(dolmen.forms.base)
    crom.configure(dolmen.forms.ztk)


def crom_teardown():
    testing.teardown()


class WSGIApplication(object):

    def __init__(self, formname):
        self.formname = formname

    @webob.dec.wsgify(RequestClass=Request)
    def __call__(self, req):
        context = Location()
        directlyProvides(context, IPublicationRoot)
        form = Interface(context, req, name=self.formname)
        return form()


@pytest.fixture(autouse=True, scope="module")
def crom_environ():
    crom_setup()
    yield
    crom_teardown()


@pytest.fixture(scope='session')
def wsgi_application(request):
    return WSGIApplication
