# -*- coding: utf-8 -*-

import crom

from dolmen.forms.base.interfaces import IWidget
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


@crom.adapter
@crom.target(IWidget)
@crom.sources(TextSchemaField, Interface, Interface)
class TextFieldWidget(SchemaFieldWidget):
    template = getTemplate('textfieldwidget.pt')


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(TextSchemaField, Interface, Interface)
class TextDisplayWidget(SchemaFieldWidget):
    template = getTemplate('textdisplaywidget.pt')
