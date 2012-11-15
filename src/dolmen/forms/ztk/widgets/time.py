# -*- coding: utf-8 -*-

import grokcore.component as grok

from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import DisplayFieldWidget
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from dolmen.forms.ztk.fields import registerSchemaField

from zope.i18n.format import DateTimeParseError
from zope.i18n.interfaces.locales import ILocale
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(TimeSchemaField, schema_interfaces.ITime)


class TimeSchemaField(SchemaField):
    """A time field.
    """


class TimeFieldWidget(SchemaFieldWidget):
    grok.adapts(TimeSchemaField, Interface, Interface)

    valueType = 'time'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType, 'short')
        return formatter.format(value)


class TimeWidgetExtractor(WidgetExtractor):
    grok.adapts(TimeSchemaField, Interface, Interface)

    valueType = 'time'

    def extract(self):
        value, error = super(TimeWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            if value:
                locale = ILocale(self.request)
                formatter = locale.dates.getFormatter(self.valueType, 'short')
                try:
                    value = formatter.parse(value)
                except (ValueError, DateTimeParseError), error:
                    return None, str(error)
            else:
                value = None
        return value, error


class HiddenTimeWidgetExtractor(TimeWidgetExtractor):
    grok.name('hidden')


class TimeFieldDisplayWidget(DisplayFieldWidget):
    grok.adapts(TimeSchemaField, Interface, Interface)

    valueType = 'time'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType)
        return formatter.format(value)
