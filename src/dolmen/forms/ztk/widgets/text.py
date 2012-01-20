# -*- coding: utf-8 -*-

from grokcore import component as grok
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from dolmen.forms.ztk.fields import registerSchemaField
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(TextSchemaField, schema_interfaces.IText)


class TextSchemaField(SchemaField):
    """A text field.
    """


class TextFieldWidget(SchemaFieldWidget):
    grok.adapts(TextSchemaField, Interface, Interface)
    template = getTemplate('textfieldwidget.pt')


class TextDisplayWidget(SchemaFieldWidget):
    grok.adapts(TextSchemaField, Interface, Interface)
    grok.name('display')
    template = getTemplate('textdisplaywidget.pt')
