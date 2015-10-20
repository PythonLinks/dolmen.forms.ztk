# -*- coding: utf-8 -*-


import hashlib
md5hash = lambda s: hashlib.md5(s).hexdigest()

import crom

from dolmen.forms.base.interfaces import IWidget, IWidgetExtractor
from dolmen.forms.base import _, Fields, Widgets, cloneFormData
from dolmen.forms.base.datamanagers import NoneDataManager
from dolmen.forms.base.interfaces import IField, IWidget, IWidgetExtractor
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor, createWidget

from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.interfaces import ICollectionSchemaField
from dolmen.forms.ztk.widgets.choice import ChoiceSchemaField, ChoiceFieldWidget
from dolmen.forms.ztk.widgets.object import ObjectSchemaField
from dolmen.forms.ztk.fields import (
    SchemaField, registerSchemaField, SchemaFieldWidget)

from zope.interface import Interface, implementer
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(CollectionSchemaField, schema_interfaces.ICollection)
    registerSchemaField(ListSchemaField, schema_interfaces.IList)
    registerSchemaField(SetSchemaField, schema_interfaces.ISet)
    registerSchemaField(TupleSchemaField, schema_interfaces.ITuple)


@implementer(ICollectionSchemaField)
class CollectionSchemaField(SchemaField):
    """A collection field.
    """
    collectionType = list
    allowAdding = True
    allowRemove = True

    def __init__(self, field):
        super(CollectionSchemaField, self).__init__(field)
        self.__value_field = IField(self._field.value_type)

    @property
    def valueField(self):
        return self.__value_field

    def isEmpty(self, value):
        return value is NO_VALUE or not len(value)


class ListSchemaField(CollectionSchemaField):
    """A list field
    """
    collectionType = list
    allowOrdering = True


class SetSchemaField(CollectionSchemaField):
    """A set field
    """
    collectionType = set


class TupleSchemaField(CollectionSchemaField):
    """A tuple field.
    """
    collectionType = tuple


def newCollectionWidgetFactory(mode=u"", interface=IWidget):
    def collectionWidgetFactory(field, form, request):
        """A widget of a collection is a bit advanced. We have to adapt
        the sub-type of the field as well.
        """
        return interface(field, field.valueField, form, request, name=mode)
    return collectionWidgetFactory


@crom.adapter
@crom.name('input')
@crom.target(IWidget)
@crom.sources(ICollectionSchemaField, Interface, Interface)
def input_collection(field, form, request):
    return newCollectionWidgetFactory(mode='input')(field, form, request)


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(ICollectionSchemaField, Interface, Interface)
def display_collection(field, form, request):
    return newCollectionWidgetFactory(mode='display')(field, form, request)


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(ICollectionSchemaField, Interface, Interface)
def extractor_collection(field, form, request):
    return newCollectionWidgetFactory(
        interface=IWidgetExtractor)(field, form, request)



@crom.adapter
@crom.target(IWidget)
@crom.sources(ICollectionSchemaField, Interface, Interface, Interface)
class MultiGenericFieldWidget(SchemaFieldWidget):

    allowAdding = True
    allowRemove = True

    template = getTemplate('multigenericfieldwidget.pt')

    def __init__(self, field, value_field, form, request):
        super(MultiGenericFieldWidget, self).__init__(field, form, request)
        self.allowAdding = field.allowAdding
        self.allowRemove = field.allowRemove
        self.valueField = value_field
        self.valueWidgets = Widgets()
        self.haveValues = False

    def createValueWidget(self, new_identifier, value):
        field = self.valueField.clone(new_identifier=str(new_identifier))
        form = cloneFormData(self.form, prefix=self.identifier)
        if value is not None:
            form.ignoreContent = False
            form.setContentData(NoneDataManager(value))
        else:
            form.ignoreRequest = False
            form.ignoreContent = True
        return createWidget(field, form, self.request)

    def addValueWidget(self, new_identifier, value):
        widget = self.createValueWidget(new_identifier, value)
        if widget is not None:
            self.valueWidgets.append(widget)
        return widget

    def prepareContentValue(self, values):
        if values is NO_VALUE:
            return {self.identifier: '0'}
        for position, value in enumerate(values):
            # Create new widgets for each value
            self.addValueWidget(position, value)
        count = len(values)
        if count:
            self.haveValues = True
        return {self.identifier: str(count)}

    def prepareRequestValue(self, values):
        value_count = 0
        identifier_count = int(values.get(self.identifier, '0'))
        remove_something = self.identifier + '.remove' in values
        for position in range(0, identifier_count):
            value_marker = (self.identifier, position,)
            value_present = '%s.present.%d' % value_marker in values
            if not value_present:
                continue
            value_selected = '%s.checked.%d' % value_marker in values
            if remove_something and value_selected:
                continue
            self.addValueWidget(position, None)
            value_count += 1
        if self.identifier + '.add' in values:
            self.addValueWidget(identifier_count, None)
            value_count += 1
            values[self.identifier] = str(identifier_count + 1)
        if value_count:
            self.haveValues = True
        return values

    @property
    def jsonTemplateWidget(self):
        widgets = Widgets()
        widgets.append(self.createValueWidget('{identifier}', None))
        widgets.update()
        return list(widgets)[0]

    def update(self):
        super(MultiGenericFieldWidget, self).update()
        self.valueWidgets.update()

        self.jsonAddIdentifier = None
        self.jsonAddTemplate = None
        self.includeEmptyMessage = self.allowRemove
        if self.allowAdding:
            self.jsonAddIdentifier = 'id' + md5hash(self.identifier)
            widgets = Widgets()
            widgets.append(self.createValueWidget(
                    '{' + self.jsonAddIdentifier + '}', None))
            widgets.update()
            self.jsonAddTemplate = list(widgets)[0]


@crom.adapter
@crom.target(IWidget)
@crom.sources(ListSchemaField, Interface, Interface, Interface)
class ListGenericFieldWidget(MultiGenericFieldWidget):

    def __init__(self, field, value_field, form, request):
        super(ListGenericFieldWidget, self).__init__(
            field, value_field, form, request)
        self.allowOrdering = field.allowOrdering


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(ICollectionSchemaField, Interface, Interface, Interface)
class MultiGenericDisplayFieldWidget(MultiGenericFieldWidget):
    template = getTemplate('multigenericdisplayfieldwidget.pt')


# For collection of objects, generate a different widget (with a table)

@crom.adapter
@crom.target(IWidget)
@crom.sources(ICollectionSchemaField, ObjectSchemaField, Interface, Interface)
class MultiObjectFieldWidget(MultiGenericFieldWidget):

    template = getTemplate('multiobjectfieldwidget.pt')

    def getFields(self):
        return self.valueField.objectFields


@crom.adapter
@crom.target(IWidget)
@crom.sources(ListSchemaField, ObjectSchemaField, Interface, Interface)
class ListObjectFieldWidget(MultiObjectFieldWidget):

    template = getTemplate('listobjectfieldwidget.pt')

    def __init__(self, field, value_field, form, request):
        super(ListObjectFieldWidget, self).__init__(
            field, value_field, form, request)
        self.allowOrdering = field.allowOrdering


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(ICollectionSchemaField, Interface, Interface, Interface)
class MultiGenericWidgetExtractor(WidgetExtractor):

    def __init__(self, field, value_field, form, request):
        super(MultiGenericWidgetExtractor, self).__init__(
            field, form, request)
        self.valueField = value_field

    def extract(self):
        value = self.request.form.get(self.identifier, NO_VALUE)
        if value is not NO_VALUE:
            try:
                value = int(value)
            except ValueError:
                return (None, u"Invalid internal input")
            collectedValues = []
            for position in range(0, int(value)):
                value_present = '%s.present.%d' % (
                    self.identifier, position) in self.request.form
                if not value_present:
                    # This value have been removed
                    continue
                field = self.valueField.clone(new_identifier=str(position))
                form = cloneFormData(self.form, prefix=self.identifier)
                data, errors = form.extractData(Fields(field))
                if errors:
                    return (None, errors)
                collectedValues.append(data[field.identifier])
            value = self.component.collectionType(collectedValues)
        return (value, None)


# Multi-Choice widget

@crom.adapter
@crom.target(IWidget)
@crom.sources(SetSchemaField, ChoiceSchemaField, Interface, Interface)
class MultiChoiceFieldWidget(ChoiceFieldWidget):

    template = getTemplate('multichoicefieldwidget.pt')

    def __init__(self, field, value_field, form, request):
        super(MultiChoiceFieldWidget, self).__init__(field, form, request)
        self.source = value_field

    def prepareContentValue(self, value):
        form_value = []
        if value is NO_VALUE:
            return {self.identifier: form_value}
        choices = self.choices()
        for entry in value:
            try:
                term = choices.getTerm(entry)
                form_value.append(term.token)
            except LookupError:
                pass
        return {self.identifier: form_value}

    def renderableChoice(self):
        current = self.inputValue()
        base_id = self.htmlId()
        for i, choice in enumerate(self.choices()):
            yield {'token': choice.token,
                   'title': choice.title,
                   'checked': choice.token in current,
                   'id': base_id + '-' + str(i)}


@crom.adapter
@crom.name('multiselect')
@crom.target(IWidget)
@crom.sources(ICollectionSchemaField, Interface, Interface)
def multiselect_collection(field, form, request):
    return newCollectionWidgetFactory(mode='multiselect')(field, form, request)


@crom.adapter
@crom.name('multiselect')
@crom.target(IWidget)
@crom.sources(SetSchemaField, ChoiceSchemaField, Interface, Interface)
class MultiSelectFieldWidget(MultiChoiceFieldWidget):
    template = getTemplate('multiselectfieldwidget.pt')


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(SetSchemaField, ChoiceSchemaField, Interface, Interface)
class MultiChoiceDisplayFieldWidget(MultiChoiceFieldWidget):
    template = getTemplate('multichoicedisplayfieldwidget.pt')

    def renderableChoice(self):
        current = self.inputValue()
        base_id = self.htmlId()
        for i, choice in enumerate(self.choices()):
            if choice.token in current:
                yield {'title': choice.title,
                       'id': base_id + '-' + str(i)}


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(SetSchemaField, ChoiceSchemaField, Interface, Interface)
class MultiChoiceWidgetExtractor(WidgetExtractor):

    def __init__(self, field, value_field, form, request):
        super(MultiChoiceWidgetExtractor, self).__init__(field, form, request)
        self.source = value_field

    def extract(self):
        value, errors = super(MultiChoiceWidgetExtractor, self).extract()
        if errors is None:
            is_present = self.request.form.get(
                self.identifier + '.present', NO_VALUE)
            if is_present is NO_VALUE:
                # Not in the request
                return (NO_VALUE, None)
            if value is NO_VALUE:
                # Nothing selected
                return (self.component.collectionType(), None)
            choices = self.source.getChoices(self.form.context)
            try:
                if not isinstance(value, list):
                    value = [value]
                value = self.component.collectionType(
                    [choices.getTermByToken(t).value for t in value])
            except LookupError:
                return (None, _(u'The selected value is not available.'))
        return (value, errors)
