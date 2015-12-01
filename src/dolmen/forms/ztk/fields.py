# -*- coding: utf-8 -*-

from cromlech.browser.interfaces import IRequest
from grokcore import component as grok

from dolmen.forms.base import interfaces, _
from dolmen.forms.base.fields import Field
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import FieldWidget, WidgetExtractor
from dolmen.forms.base.interfaces import IFieldExtractionValueSetting

from dolmen.forms.ztk.interfaces import ISchemaField

from zope import schema, component
from zope.interface import Interface, Invalid
from zope.interface.interfaces import IInterface
from zope.schema import interfaces as schema_interfaces
from zope.schema._bootstrapinterfaces import IContextAwareDefaultFactory


class SchemaFieldFactory(object):
    """Create form fields from a zope.schema field (by adapting it).
    """
    grok.implements(interfaces.IFieldFactory)

    def __init__(self, context):
        self.context = context

    def produce(self):
        interface = self.context.interface
        if not interface and not getattr(self.context, '__name__', None):
            raise ValueError("Field has no interface")
        yield interfaces.IField(self.context)


class InterfaceSchemaFieldFactory(object):
    """Create a set of form fields from a zope.interface by looking
    each zope.schema fields defined on it and adapting them.
    """
    grok.implements(interfaces.IFieldFactory)

    def __init__(self, context):
        self.context = context

    def produce(self):
        for name, field in schema.getFieldsInOrder(self.context):
            yield interfaces.IField(field)


class BaseField(Field):

    def getDefaultValue(self, form):
        if self.defaultFactory is not None:
            if IContextAwareDefaultFactory.providedBy(self.defaultFactory):
                default = self.defaultFactory(form.getContent()) 
            else: 
                default = self.defaultFactory()
        else:
            default = super(BaseField, self).getDefaultValue(form)

        if default is NO_VALUE:
            default = self.defaultValue

        if default is None:
            return NO_VALUE

        return default

    
class SchemaField(Field):
    """A form field using a zope.schema field as settings.
    """
    grok.implements(ISchemaField)

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
        error = super(SchemaField, self).validate(value, context)
        if error is not None:
            return error

        if value is not NO_VALUE:
            try:
                binded_field = self._field.bind(context)
                binded_field.validate(value)
            except schema_interfaces.ValidationError, error:
                return error.doc()
            except Invalid, error:
                return error.args[0]
        return None

    def fromUnicode(self, value):
        if schema_interfaces.IFromUnicode.providedBy(self._field):
            return self._field.fromUnicode(value)
        return value

    
def registerSchemaField(factory, schema_field):
    # We register it by hand to have the adapter available when loading ZCML.
    component.provideAdapter(factory, (schema_field,), interfaces.IField)


class SchemaFieldWidget(FieldWidget):
    grok.adapts(ISchemaField, Interface, Interface)

    def htmlClass(self):
        css_class = ['field']
        css_class.append('field-%s' % (
                self.component._field.__class__.__name__.lower()))
        if self.required:
            css_class.append('field-required')
        return ' '.join(css_class)


class SchemaWidgetExtractor(WidgetExtractor):
    grok.adapts(ISchemaField,
                IFieldExtractionValueSetting,
                IRequest)

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
            except schema_interfaces.ValidationError, e:
                return None, e.doc()
            except Invalid, e:
                return None, e.args[0]
            except ValueError, e:
                return None, _(u"Invalid value.")

        return value, None


def registerDefault():
    """Register default fields factories.
    """
    component.provideAdapter(SchemaFieldFactory, (schema.interfaces.IField,))
    component.provideAdapter(InterfaceSchemaFieldFactory, (IInterface,))
    registerSchemaField(SchemaField, schema_interfaces.IField)
