# -*- coding: utf-8 -*-

from grokcore import component as grok
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import registerSchemaField
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(PasswordField, schema_interfaces.IPassword)


class PasswordField(SchemaField):
    """A password field.
    """


class PasswordWidget(SchemaFieldWidget):
    grok.adapts(PasswordField, None, None)
    template = getTemplate('passwordwidget.pt')
