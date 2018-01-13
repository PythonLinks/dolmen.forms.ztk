# -*- coding: utf-8 -*-

import crom

from cromlech.content import IFactory
from dolmen.forms.base import interfaces, cloneFormData, Fields, Widgets
from dolmen.forms.base.datamanagers import ObjectDataManager
from dolmen.forms.base.markers import NO_VALUE, Marker
from dolmen.forms.base.widgets import WidgetExtractor

from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.interfaces import IObjectSchemaField
from dolmen.forms.ztk.fields import (
    SchemaField, registerSchemaField, SchemaFieldWidget)

from zope.interface import Interface, implementer
from zope.schema import interfaces as schema_interfaces
from zope import schema


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


@implementer(IObjectSchemaField)
class ObjectSchemaField(SchemaField):
    """A collection field.
    """
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
        return IFactory.component(name=schema.__identifier__)


@crom.adapter
@crom.target(interfaces.IWidget)
@crom.sources(ObjectSchemaField, Interface, Interface)
class ObjectFieldWidget(SchemaFieldWidget):

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


@crom.adapter
@crom.target(interfaces.IWidgetExtractor)
@crom.sources(ObjectSchemaField, Interface, Interface)
class ObjectFieldExtractor(WidgetExtractor):

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
            value = factory(**{
                k:v for k, v in data.items() if not isinstance(v, Marker)})
            return (value, None)
        return (value, errors)
