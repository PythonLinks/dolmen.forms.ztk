# URI widget

import crom

from dolmen.forms.base.interfaces import IWidget
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import (
    SchemaField, SchemaFieldWidget, registerSchemaField)

from zope.schema import interfaces as schema_interfaces
from zope.interface import Interface


def register():
    registerSchemaField(URISchemaField, schema_interfaces.IURI)


class URISchemaField(SchemaField):
    """A text line field.
    """

@crom.adapter
@crom.name('input')
@crom.target(IWidget)
@crom.sources(URISchemaField, Interface, Interface)
class URIWidget(SchemaFieldWidget):
    template = getTemplate('uriwidget.pt')
