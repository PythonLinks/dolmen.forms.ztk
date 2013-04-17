# -*- coding: utf-8 -*-

import crom
from cromlech.i18n import ILocale
from dolmen.forms.base.interfaces import IWidget, IWidgetExtractor
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import DisplayFieldWidget
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from dolmen.forms.ztk.fields import registerSchemaField
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces
from babel.dates import format_time, parse_time


def register():
    registerSchemaField(TimeSchemaField, schema_interfaces.ITime)


class TimeSchemaField(SchemaField):
    """A time field.
    """


@crom.adapter
@crom.target(IWidget)
@crom.sources(TimeSchemaField, Interface, Interface)
class TimeFieldWidget(SchemaFieldWidget):

    def valueToUnicode(self, value):
        locale = ILocale(self.request, default='en')
        return format_time(value, locale=str(locale))


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(TimeSchemaField, Interface, Interface)
class TimeWidgetExtractor(WidgetExtractor):

    def extract(self):
        value, error = super(TimeWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            if value:
                try:
                    locale = ILocale(self.request, default='en')
                    value = parse_time(value, locale=str(locale))
                    return value, error
                except (ValueError, IndexError), err:
                    return None, 'Unknown time pattern'
            else:
                value = None
        return value, error


@crom.adapter
@crom.name('hidden')
@crom.target(IWidgetExtractor)
@crom.sources(TimeSchemaField, Interface, Interface)
class HiddenTimeWidgetExtractor(TimeWidgetExtractor):
    pass


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(TimeSchemaField, Interface, Interface)
class TimeFieldDisplayWidget(DisplayFieldWidget):

    def valueToUnicode(self, value):
        locale = ILocale(self.request, default='en')
        return format_time(value, locale=str(locale))
