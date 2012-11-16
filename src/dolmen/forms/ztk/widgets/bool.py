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
        is_present = self.request.form.get(
            self.identifier + '.present', NO_VALUE)

        if is_present is NO_VALUE:
            value = NO_VALUE
        elif is_present is not NO_VALUE and value == u'True':
            value = True
        else:
            value = False
        return (value, error)


class HiddenCheckBoxWidgetExtractor(CheckBoxWidgetExtractor):
    grok.name('hidden')


def register():
    """Entry point hook.
    """
    registerSchemaField(BooleanSchemaField, schema_interfaces.IBool)
