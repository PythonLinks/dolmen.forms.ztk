# -*- coding: utf-8 -*-

from dolmen.forms.ztk.fields import (SchemaField, registerSchemaField,
                                     SchemaWidgetExtractor)
from grokcore import component as grok
from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(FloatSchemaField, schema_interfaces.IFloat)
    registerSchemaField(IntSchemaField, schema_interfaces.IInt)


class IntSchemaField(SchemaField):
    """A integer field.
    """
    def fromUnicode(self, value):
        if value is not None:
            return self._field.fromUnicode(value)
        return value


class FloatSchemaField(SchemaField):
    """A float field.
    """
    def fromUnicode(self, value):
        if value is not None:
            return self._field.fromUnicode(value)
        return value


class IntWidgetExtractor(SchemaWidgetExtractor):
    grok.adapts(IntSchemaField, Interface, Interface)
    empty_is_None = True


class HiddenIntWidgetExtractor(IntWidgetExtractor):
    grok.name('hidden')


class FloatWidgetExtractor(SchemaWidgetExtractor):
    grok.adapts(FloatSchemaField, Interface, Interface)
    empty_is_None = True


class HiddenFloatWidgetExtractor(FloatWidgetExtractor):
    grok.name('hidden')
