# -*- coding: utf-8 -*-

import crom
from dolmen.forms.base import interfaces
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import DisplayFieldWidget, WidgetExtractor
from dolmen.forms.ztk.fields import (
    SchemaField, SchemaFieldWidget, registerSchemaField)

from zope.i18n.format import DateTimeParseError
from zope.i18n.interfaces.locales import ILocale
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


@crom.adapter
@crom.target(interfaces.IWidget)
@crom.sources(DateSchemaField, Interface, Interface)
class DateFieldWidget(SchemaFieldWidget):

    valueType = 'date'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType, 'short')
        return formatter.format(value)


@crom.adapter
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DateSchemaField, Interface, Interface)
class DateWidgetExtractor(WidgetExtractor):

    valueType = 'date'

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
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


@crom.adapter
@crom.name('hidden')
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DateSchemaField, Interface, Interface)
class HiddenDateWidgetExtractor(DateWidgetExtractor):
    pass


@crom.adapter
@crom.target(interfaces.IWidget)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class DatetimeFieldWidget(DateFieldWidget):
    valueType = 'dateTime'


@crom.adapter
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class DatetimeWidgetExtractor(DateWidgetExtractor):
    valueType = 'dateTime'


@crom.adapter
@crom.name('hidden')
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class HiddenDatetimeWidgetExtractor(DatetimeWidgetExtractor):
    pass



@crom.adapter
@crom.name('display')
@crom.target(interfaces.IWidget)
@crom.sources(DateSchemaField, Interface, Interface)
class DateFieldDisplayWidget(DisplayFieldWidget):

    valueType = 'date'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType)
        return formatter.format(value)


@crom.adapter
@crom.name('display')
@crom.target(interfaces.IWidget)
@crom.sources(DatetimeSchemaField, Interface, Interface)
class DatetimeFieldDisplayWidget(DateFieldDisplayWidget):
    valueType = 'dateTime'
