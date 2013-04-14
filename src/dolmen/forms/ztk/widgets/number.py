# -*- coding: utf-8 -*-

import crom
from dolmen.forms.base.interfaces import IWidgetExtractor
from dolmen.forms.ztk.fields import (
    SchemaField, registerSchemaField, SchemaWidgetExtractor)
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


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(IntSchemaField, Interface, Interface)
class IntWidgetExtractor(SchemaWidgetExtractor):
    empty_is_None = True


@crom.adapter
@crom.name('hidden')
@crom.target(IWidgetExtractor)
@crom.sources(IntSchemaField, Interface, Interface)
class HiddenIntWidgetExtractor(SchemaWidgetExtractor):
    empty_is_None = True



@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(FloatSchemaField, Interface, Interface)
class FloatWidgetExtractor(SchemaWidgetExtractor):
    empty_is_None = True


@crom.adapter
@crom.name('hidden')
@crom.target(IWidgetExtractor)
@crom.sources(FloatSchemaField, Interface, Interface)
class HiddenFloatWidgetExtractor(SchemaWidgetExtractor):
    empty_is_None = True
