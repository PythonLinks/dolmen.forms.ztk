# Text line widget

import crom
from dolmen.forms.base.interfaces import IWidget
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import (
    SchemaField, SchemaFieldWidget, registerSchemaField)
from zope.schema import interfaces as schema_interfaces
from zope.interface import Interface


def register():
    registerSchemaField(TextLineSchemaField, schema_interfaces.ITextLine)


class TextLineSchemaField(SchemaField):
    """A text line field.
    """

@crom.adapter
@crom.target(IWidget)
@crom.sources(TextLineSchemaField, Interface, Interface)
class TextLineWidget(SchemaFieldWidget):
    template = getTemplate('textlinewidget.pt')
    defaultHtmlClass = ['field', 'field-textline']
    defaultHtmlAttributes = set(['readonly', 'required', 'autocomplete',
                                 'maxlength', 'pattern', 'placeholder',
                                 'size', 'style', 'disabled'])
