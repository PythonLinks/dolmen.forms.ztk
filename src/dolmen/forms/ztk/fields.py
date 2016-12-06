# -*- coding: utf-8 -*-

import crom
from crom.implicit import implicit
from cromlech.browser.interfaces import IRequest

from dolmen.forms.base import interfaces, _
from dolmen.forms.base.fields import Field
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import FieldWidget, WidgetExtractor
from dolmen.forms.base.interfaces import IFieldExtractionValueSetting
from dolmen.forms.ztk.interfaces import ISchemaField

from zope import schema
from zope.interface import Interface, Invalid, implementer
from zope.interface.interfaces import IInterface
from zope.schema import interfaces as schema_interfaces


@implementer(interfaces.IFieldFactory)
class SchemaFieldFactory(object):
    """Create form fields from a zope.schema field (by adapting it).
    """

    def __init__(self, context):
        self.context = context

    def produce(self):
        interface = self.context.interface
        if not interface and not getattr(self.context, '__name__', None):
            raise ValueError("Field has no interface")
        yield interfaces.IField(self.context)


@implementer(interfaces.IFieldFactory)
class InterfaceSchemaFieldFactory(object):
    """Create a set of form fields from a zope.interface by looking
    each zope.schema fields defined on it and adapting them.
    """

    def __init__(self, context):
        self.context = context

    def produce(self):
        for name, field in schema.getFieldsInOrder(self.context):
            yield interfaces.IField(field)


@implementer(ISchemaField)
class SchemaField(Field):
    """A form field using a zope.schema field as settings.
    """

    def __init__(self, field):
        super(SchemaField, self).__init__(
            field.title or None, field.__name__)
        self.description = field.description
        self.required = field.required
        self.readonly = field.readonly
        self._field = field

    def get_field(self):
        return self._field

    def clone(self, new_identifier=None):
        copy = self.__class__(self._field)
        copy.__dict__.update(self.__dict__)
        if new_identifier is not None:
            copy.identifier = new_identifier
        return copy

    def validate(self, value, context=None):
        error = super(SchemaField, self).validate(value)
        if error is not None:
            return error

        if value is not NO_VALUE:
            try:
                binded_field = self._field.bind(context)
                binded_field.validate(value)
            except schema_interfaces.ValidationError as error:
                return error.doc()
            except Invalid as error:
                return error.args[0]
        return None

    def fromUnicode(self, value):
        if schema_interfaces.IFromUnicode.providedBy(self._field):
            return self._field.fromUnicode(value)
        return value

    def getDefaultValue(self, form):
        default = super(SchemaField, self).getDefaultValue(form)
        if default is not NO_VALUE:
            return default
        default = self._field.default
        if default is None:     # Zope schema use None to say no default
            return NO_VALUE
        return default


def registerSchemaField(factory, schema_field, registry=None):
    # We register it by hand to have the adapter available when loading ZCML.
    if registry is None:
        registry = implicit.registry
    registry.register((schema_field,), interfaces.IField, u'', factory)


@crom.adapter
@crom.target(interfaces.IWidget)
@crom.sources(ISchemaField, Interface, Interface)
class SchemaFieldWidget(FieldWidget):
    pass


@crom.adapter
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(ISchemaField, IFieldExtractionValueSetting, IRequest)
class SchemaWidgetExtractor(WidgetExtractor):

    empty_is_None = False

    def extract(self):
        value, error = super(SchemaWidgetExtractor, self).extract()
        if self.empty_is_None and hasattr(value, '__len__') and not len(value):
            value = None
        if error is not None:
            return value, error

        if value is not NO_VALUE:
            try:
                value = self.component.fromUnicode(value)
            except schema_interfaces.ValidationError as e:
                return None, e.doc()
            except Invalid as e:
                return None, e.args[0]
            except ValueError as e:
                return None, _(u"Invalid value.")

        return value, None


@crom.adapter
@crom.name('hidden')
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(ISchemaField, IFieldExtractionValueSetting, IRequest)
class HiddenSchemaWidgetExtractor(SchemaWidgetExtractor):
    pass


@crom.adapter
@crom.name('readonly')
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(ISchemaField, IFieldExtractionValueSetting, IRequest)
class ReadOnlySchemaWidgetExtractor(SchemaWidgetExtractor):
    pass


def registerDefault(registry=None):
    """Register default fields factories.
    """
    if registry is None:
        registry = implicit.registry

    registry.register(
        (schema.interfaces.IField,),
        interfaces.IFieldFactory, u'', SchemaFieldFactory)

    registry.register(
        (IInterface,),
        interfaces.IFieldFactory, u'', InterfaceSchemaFieldFactory)

    registerSchemaField(
        SchemaField, schema_interfaces.IField, registry=registry)
