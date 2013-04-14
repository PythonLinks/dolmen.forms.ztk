# -*- coding: utf-8 -*-

import crom
from dolmen.forms.base import _
from dolmen.forms.base.interfaces import IWidget, IWidgetExtractor
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor, DisplayFieldWidget
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from dolmen.forms.ztk.fields import registerSchemaField
from zope.schema import interfaces as schema_interfaces
from zope.interface import Interface


class BooleanSchemaField(SchemaField):
    """A boolean field.
    """

@crom.adapter
@crom.target(IWidget)
@crom.sources(BooleanSchemaField, Interface, Interface)
class CheckBoxWidget(SchemaFieldWidget):
    template = getTemplate('checkboxwidget.pt')


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(BooleanSchemaField, Interface, Interface)
class CheckBoxDisplayWidget(DisplayFieldWidget):

    def valueToUnicode(self, value):
        if bool(value):
            return _(u'Yes')
        return _(u'No')


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(BooleanSchemaField, Interface, Interface)
class CheckBoxWidgetExtractor(WidgetExtractor):

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


@crom.adapter
@crom.name('hidden')
@crom.target(IWidgetExtractor)
@crom.sources(BooleanSchemaField, Interface, Interface)
class HiddenCheckBoxWidgetExtractor(CheckBoxWidgetExtractor):
    pass


def register():
    """Entry point hook.
    """
    registerSchemaField(BooleanSchemaField, schema_interfaces.IBool)
