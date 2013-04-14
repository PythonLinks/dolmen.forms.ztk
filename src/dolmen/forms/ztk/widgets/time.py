# -*- coding: utf-8 -*-

import crom
from dolmen.forms.base.interfaces import IWidget, IWidgetExtractor
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


@crom.adapter
@crom.target(IWidget)
@crom.sources(TimeSchemaField, Interface, Interface)
class TimeFieldWidget(SchemaFieldWidget):

    valueType = 'time'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType, 'short')
        return formatter.format(value)


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(TimeSchemaField, Interface, Interface)
class TimeWidgetExtractor(WidgetExtractor):

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

    valueType = 'time'

    def valueToUnicode(self, value):
        locale = ILocale(self.request)
        formatter = locale.dates.getFormatter(self.valueType)
        return formatter.format(value)
