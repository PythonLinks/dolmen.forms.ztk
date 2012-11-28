# -*- coding: utf-8 -*-

from dolmen.forms.base import cloneFormData, Fields, Widgets
from dolmen.forms.base.datamanagers import ObjectDataManager
from dolmen.forms.base.markers import NO_VALUE, Marker
from dolmen.forms.base.widgets import WidgetExtractor

from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.interfaces import IObjectSchemaField
from dolmen.forms.ztk.fields import (
    SchemaField, registerSchemaField, SchemaFieldWidget)

from zope.component import getUtility
from zope.component.interfaces import IFactory
from zope.interface import Interface, implements
from zope.schema import interfaces as schema_interfaces
from zope import schema

from grokcore import component as grok


def register():
    registerSchemaField(ObjectSchemaField, schema_interfaces.IObject)


class BindedSchema(object):

    def __init__(self, schema, context):
        self.schema = schema
        self.context = context

    # we redefine getitem
    def __getitem__(self, name):
        attr = self.schema[name]
        return attr.bind(self.context)

    # but let all the rest slip to schema
    def __getattr__(self, name):
        return getattr(self.schema, name)


class Object(schema.Object):
    """inherit schema.Object but binds correctly"""

    def bind(self, context=None):
        binded = super(Object, self).bind(context)
        binded.schema = BindedSchema(self.schema, context)
        return binded


class ObjectSchemaField(SchemaField):
    """A collection field.
    """
    implements(IObjectSchemaField)
    objectFactory = None
    dataManager = ObjectDataManager

    def __init__(self, field):
        super(ObjectSchemaField, self).__init__(field)
        self.schema = field.schema
        self.__object_fields = Fields(self.schema)

    @property
    def objectSchema(self):
        return self.schema

    @property
    def objectFields(self):
        return self.__object_fields

    def getObjectFactory(self):
        if self.objectFactory is not None:
            return self.objectFactory
        schema = self.objectSchema
        return getUtility(IFactory, name=schema.__identifier__)


class ObjectFieldWidget(SchemaFieldWidget):
    grok.adapts(ObjectSchemaField, Interface, Interface)

    template = getTemplate('objectfieldwidget.pt')

    def prepareContentValue(self, value):
        if value is NO_VALUE:
            return {self.identifier: []}
        return {self.identifier: value}

    def update(self):
        super(ObjectFieldWidget, self).update()
        value = self.component.dataManager(self.inputValue())
        form = cloneFormData(self.form, value, self.identifier)
        self.objectWidgets = Widgets(form=form, request=self.request)
        self.objectWidgets.extend(self.component.objectFields)
        self.objectWidgets.update()


class ObjectFieldExtractor(WidgetExtractor):
    grok.adapts(ObjectSchemaField, Interface, Interface)

    def extract(self):
        is_present = self.request.form.get(self.identifier, NO_VALUE)
        if is_present is NO_VALUE:
            return (NO_VALUE, None)
        value = None
        form = cloneFormData(self.form, None, self.identifier)
        data, errors = form.extractData(self.component.objectFields)
        if not errors:
            factory = self.component.getObjectFactory()
            # Create an object with values
            value = factory(**dict(filter(
                        lambda (k, v): not isinstance(v, Marker),
                        data.items())))
            return (value, None)
        return (value, errors)
