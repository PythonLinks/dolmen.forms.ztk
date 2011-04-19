# -*- coding: utf-8 -*-

from dolmen.forms.base import _
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import DisplayFieldWidget, WidgetExtractor

from dolmen.forms.ztk.fields import (
    SchemaField, SchemaFieldWidget, registerSchemaField)

from grokcore import component as grok

from zope.i18n.format import DateTimeParseError
from zope.i18n.interfaces.locales import ILocale
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(DatetimeSchemaField, schema_interfaces.IDatetime)
    registerSchemaField(DateSchemaField, schema_interfaces.IDate)


class DatetimeSchemaField(SchemaField):
    """A datetime field.
    """


class DateSchemaField(SchemaField):
    """A date field.
    """


class DateFieldWidget(SchemaFieldWidget):
    grok.adapts(DateSchemaField, Interface, Interface)

    valueType = 'date'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType, 'short')
        return formatter.format(value)


class DateWidgetExtractor(WidgetExtractor):
    grok.adapts(DateSchemaField, Interface, Interface)

    valueType = 'date'

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            locale = ILocale(self.request)
            formatter = locale.dates.getFormatter(self.valueType, 'short')
            try:
                value = formatter.parse(value)
            except (ValueError, DateTimeParseError), error:
                return None, str(error)
        return value, error


class DatetimeFieldWidget(DateFieldWidget):
    grok.adapts(DatetimeSchemaField, Interface, Interface)

    valueType = 'dateTime'


class DatetimeWidgetExtractor(DateWidgetExtractor):
    grok.adapts(DatetimeSchemaField, Interface, Interface)

    valueType = 'dateTime'


class DateFieldDisplayWidget(DisplayFieldWidget):
    grok.adapts(DateSchemaField, Interface, Interface)

    valueType = 'date'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType)
        return formatter.format(value)


class DatetimeFieldDisplayWidget(DateFieldDisplayWidget):
    grok.adapts(DatetimeSchemaField, Interface, Interface)

    valueType = 'dateTime'
