# -*- coding: utf-8 -*-

import datetime

from dolmen.clockwork import IFormTimeManager

from dolmen.forms.base.markers import NO_VALUE, Marker
from dolmen.forms.base.widgets import FieldWidget, DisplayFieldWidget
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.fields import BaseField, registerSchemaField

from grokcore import component as grok
from zope.i18n.format import DateTimeParseError
from zope.i18nmessageid import MessageFactory
from zope.i18nmessageid.message import Message
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces


_ = MessageFactory("dolmen.forms.base")


class TimeField(BaseField):
    """A time field.
    """
    valueLength = 'short'

    def __init__(self, title,
                 min=None,
                 max=None,
                 **options):
        super(TimeField, self).__init__(title, **options)
        self.min = min
        self.max = max

    def getFormatter(self, form):
        return IFormTimeManager(form.request)

    def validate(self, value, form):
        error = super(TimeField, self).validate(value, form)
        if error is not None:
            return error
        if not isinstance(value, Marker):
            assert isinstance(value, datetime.time)
            if self.min is not None and value < self.min:
                formatter = self.getFormatter(form)
                return _(u"This time is before ${not_before}.",
                         dict(not_before=formatter.format(self.min)))
            if self.max is not None and value > self.max:
                formatter = self.getFormatter(form)
                return _(u"This time is after ${not_after}.",
                         dict(not_after=formatter.format(self.max)))
        return None

# BBB
TimeSchemaField = TimeField


class TimeFieldWidget(FieldWidget):
    grok.adapts(TimeField, Interface, Interface)
    defaultHtmlClass = ['field', 'field-time']

    def valueToUnicode(self, value):
        formatter = self.component.getFormatter(self.form)
        return formatter.format(value)


class TimeWidgetExtractor(WidgetExtractor):
    grok.adapts(TimeField, Interface, Interface)

    def extract(self):
        value, error = super(TimeWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            formatter = self.component.getFormatter(self.form)
            try:
                value = formatter.parse(value)
            except (ValueError, DateTimeParseError), error:
                error_msg = error.message
                if not isinstance(error_msg, Message):
                    error_msg = _(error_msg)
                return None, error_msg
        return value, error


class TimeFieldDisplayWidget(DisplayFieldWidget):
    grok.adapts(TimeField, Interface, Interface)

    def valueToUnicode(self, value):
        formatter = self.component.getFormatter(self.form)
        return formatter.format(value)


def TimeSchemaFactory(schema):
    field = TimeField(
        schema.title or None,
        identifier=schema.__name__,
        description=schema.description,
        required=schema.required,
        readonly=schema.readonly,
        min=schema.min,
        max=schema.max,
        interface=schema.interface,
        constrainValue=schema.constraint,
        defaultFactory=schema.defaultFactory,
        defaultValue=schema.default or NO_VALUE)
    return field

def register():
    registerSchemaField(TimeSchemaFactory, schema_interfaces.ITime)
