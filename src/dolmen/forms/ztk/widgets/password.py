# -*- coding: utf-8 -*-

import crom
from dolmen.forms.base.interfaces import IWidget
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import registerSchemaField
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from zope.schema import interfaces as schema_interfaces
from zope.interface import Interface


def register():
    registerSchemaField(PasswordField, schema_interfaces.IPassword)


class PasswordField(SchemaField):
    """A password field.
    """


@crom.adapter
@crom.target(IWidget)
@crom.sources(PasswordField, Interface, Interface)
class PasswordWidget(SchemaFieldWidget):
    template = getTemplate('passwordwidget.pt')
