# -*- coding: utf-8 -*-

import crom
from cromlech.webob.response import Response
from dolmen.forms.base import Form, Fields, action
from dolmen.forms.base import form_component, context
from zope import schema
from zope.interface import Interface, implementer


class IPerson(Interface):

    name = schema.TextLine(
        title=u"Person name")

    age = schema.Int(
        title=u"Person age",
        description=u"Age in years")


@implementer(IPerson)
class Person(object):
    name = ''
    age = 0


@form_component
@context(IPerson)
class PersonForm(Form):

    responseFactory = Response

    label = u"People form"
    description = u"Form to send people outerspace"
    fields = Fields(IPerson)

    @action(u"Send")
    def send(self):
        data, errors = self.extractData()
        self.status = u"We sent %s, age %d" % (data['name'], data['age'])
