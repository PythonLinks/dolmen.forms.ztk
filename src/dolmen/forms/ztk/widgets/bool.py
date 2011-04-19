# -*- coding: utf-8 -*-

import grokcore.component as grok

from dolmen.forms.base import _
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor, DisplayFieldWidget

from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from dolmen.forms.ztk.fields import registerSchemaField

from zope.schema import interfaces as schema_interfaces


class BooleanSchemaField(SchemaField):
    """A boolean field.
    """


class CheckBoxWidget(SchemaFieldWidget):
    grok.adapts(BooleanSchemaField, None, None)
    template = getTemplate('checkboxwidget.pt')


class CheckBoxDisplayWidget(DisplayFieldWidget):
    grok.adapts(BooleanSchemaField, None, None)

    def valueToUnicode(self, value):
        if bool(value):
            return _(u'Yes')
        return _(u'No')


class CheckBoxWidgetExtractor(WidgetExtractor):
    grok.adapts(BooleanSchemaField, None, None)

    def extract(self):
        value, error = WidgetExtractor.extract(self)
        if value is NO_VALUE:
            value = False
        elif value == 'True':
            value = True
        return (value, error)


def register():
    """Entry point hook.
    """
    registerSchemaField(BooleanSchemaField, schema_interfaces.IBool)
