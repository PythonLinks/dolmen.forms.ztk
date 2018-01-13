# -*- coding: utf-8 -*-

import crom

from dolmen.forms.base.interfaces import IWidget, IWidgetExtractor
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor

from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import (
    SchemaField, registerSchemaField, SchemaFieldWidget)

from zope.interface import Interface
from zope.schema import interfaces as schema_interfaces


def register():
    registerSchemaField(ChoiceSchemaField, schema_interfaces.IChoice)


class ChoiceSchemaField(SchemaField):
    """A choice field.
    """

    def __init__(self, field):
        super(ChoiceSchemaField, self).__init__(field)
        self.__source = None
        self.__source_name = None
        if field.source is not None:
            self.__source = field.source
        elif isinstance(field.vocabularyName, str):
            # We delay the lookup of the vocabulary, to be sure it
            # have been registered.
            self.__source = None
            self.__source_name = field.vocabularyName

    @property
    def source(self):
        if self.__source is None:
            self.__source = schema_interfaces.IVocabularyFactory.component(
                name=self.__source_name)
        return self.__source

    def getChoices(self, context):
        source = self.source
        if (schema_interfaces.IContextSourceBinder.providedBy(source) or
            schema_interfaces.IVocabularyFactory.providedBy(source)):
            source = source(context)
        assert schema_interfaces.IVocabularyTokenized.providedBy(source)
        return source


@crom.adapter
@crom.target(IWidget)
@crom.sources(ChoiceSchemaField, Interface, Interface)
class ChoiceFieldWidget(SchemaFieldWidget):

    template = getTemplate('choicefieldwidget.pt')

    def __init__(self, field, form, request):
        super(ChoiceFieldWidget, self).__init__(field, form, request)
        self.source = field
        self.__choices = None

    def lookupTerm(self, value):
        choices = self.choices()
        try:
            return choices.getTerm(value)
        except LookupError:
            # the stored value is invalid. fallback on the default one.
            default = self.component.getDefaultValue(self.form)
            if default is not NO_VALUE:
                return choices.getTerm(default)
        return None

    def valueToUnicode(self, value):
        term = self.lookupTerm(value)
        if term is not None:
            return term.token
        return u''

    def choices(self):
        if self.__choices is not None:
            return self.__choices
        # self.source is used instead of self.component in order to be
        # able to override it in subclasses.
        self.__choices = self.source.getChoices(self.form.context)
        return self.__choices


@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources(ChoiceSchemaField, Interface, Interface)
class ChoiceDisplayWidget(ChoiceFieldWidget):

    template = getTemplate('choicedisplaywidget.pt')

    def valueToUnicode(self, value):
        term = self.lookupTerm(value)
        if term is not None:
            return term.title
        return u''


@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(ChoiceSchemaField, Interface, Interface)
class ChoiceWidgetExtractor(WidgetExtractor):

    def extract(self):
        value, error = super(ChoiceWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            choices = self.component.getChoices(self.form.context)
            try:
                value = choices.getTermByToken(value).value
            except LookupError:
                return (None, u'Invalid value')
        return (value, error)


@crom.adapter
@crom.name('hidden')
@crom.target(IWidgetExtractor)
@crom.sources(ChoiceSchemaField, Interface, Interface)
class HiddenChoiceWidgetExtractor(ChoiceWidgetExtractor):
    pass


# Radio Widget
@crom.adapter
@crom.name('radio')
@crom.target(IWidget)
@crom.sources(ChoiceSchemaField, Interface, Interface)
class RadioFieldWidget(ChoiceFieldWidget):

    template = getTemplate('radiofieldwidget.pt')

    def renderableChoices(self):
        current = self.inputValue()
        base_id = self.htmlId()
        for i, choice in enumerate(self.choices()):
            yield {'token': choice.token,
                   'title': choice.title or choice.token,
                   'checked': choice.token == current and 'checked' or None,
                   'id': base_id + '-' + str(i)}
