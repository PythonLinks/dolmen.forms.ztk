# -*- coding: utf-8 -*-

from dolmen.forms.base.fields import Field
from dolmen.forms.base.widgets import FieldWidget, DisplayFieldWidget
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.fields import registerSchemaField
from dolmen.forms.ztk.widgets import getTemplate

from grokcore import component as grok
from zope.i18nmessageid import MessageFactory
from zope.schema import interfaces as schema_interfaces


_ = MessageFactory("dolmen.forms.base")


class BooleanField(Field):
    """A boolean field.
"""

# BBB
BooleanSchemaField = BooleanField


class CheckBoxWidget(FieldWidget):
    grok.adapts(BooleanField, None, None)
    defaultHtmlClass = ['field', 'field-bool']
    defaultHtmlAttributes = set(['readonly', 'style', 'disabled'])
    alternateLayout = True
    template = getTemplate('checkboxwidget.cpt')


class CheckBoxDisplayWidget(DisplayFieldWidget):
    grok.adapts(BooleanField, None, None)

    def valueToUnicode(self, value):
        if bool(value):
            return _(u'Yes')
        return _(u'No')


class CheckBoxWidgetExtractor(WidgetExtractor):
    grok.adapts(BooleanField, None, None)

    def extract(self):
        value, error = WidgetExtractor.extract(self)
        if value == 'True':
            value = True
        else:
            value = False
        return (value, error)


def BooleanSchemaFactory(schema):
    field = BooleanField(
        schema.title or None,
        identifier=schema.__name__,
        description=schema.description,
        required=schema.required,
        readonly=schema.readonly,
        interface=schema.interface,
        constrainValue=schema.constraint,
        defaultFactory=schema.defaultFactory,
        defaultValue=bool(schema.default))
    return field


def register():
    registerSchemaField(BooleanSchemaFactory, schema_interfaces.IBool)
