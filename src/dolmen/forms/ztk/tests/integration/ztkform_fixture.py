# -*- coding: utf-8 -*-

from cromlech.webob.response import Response
from dolmen.forms.ztk import Form, Fields, action
from grokcore import component as grok
from zope import interface, schema


class IPerson(interface.Interface):

    name = schema.TextLine(
        title=u"Person name")

    age = schema.Int(
        title=u"Person age",
        description=u"Age in years")


class Person(grok.Context):
    grok.implements(IPerson)


class PersonForm(Form):

    responseFactory = Response

    label = u"People form"
    description = u"Form to send people outerspace"
    fields = Fields(IPerson)

    @action(u"Send")
    def send(self):
        data, errors = self.extractData()
        self.status = u"We sent %s, age %d" % (data['name'], data['age'])
