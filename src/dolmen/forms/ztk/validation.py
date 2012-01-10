# -*- coding: utf-8 -*-

from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.ztk.interfaces import ISchemaField

from zope.interface.interfaces import IMethod
from zope.interface import directlyProvides, Invalid


class Data(object):
    """Wraps the data dicts into an object, acting as
    an attribute access proxy.
    """
    def __init__(self, interface, data, dataManager):
        self.interface = interface
        self.data = data
        self.dataManager = dataManager
        directlyProvides(self, interface)

    def __getattr__(self, name):
        try:
            field = self.interface[name]
        except KeyError:
            raise AttributeError(name)

        if IMethod.providedBy(field):
            raise RuntimeError("Data value is not a schema field", name)

        try:
            value = self.data.getWithDefault(name)
        except KeyError:
            value = NO_VALUE

        if value is NO_VALUE:
            try:
                return self.dataManager.get(name)
            except KeyError:
                # an attribute error is more sane here
                raise AttributeError(name)

        return value


class InvariantsValidation(object):
    """Validates the invariants of the given fields' interfaces.
    """
    def __init__(self, fields, form):
        self.interfaces = []
        for field in fields:
            if ISchemaField.providedBy(field):
                interface = field._field.interface
                if interface not in self.interfaces:
                    self.interfaces.append(interface)
        self.form = form


    def validate(self, data):
        errors = []
        manager = self.form.getContentData()
        for interface in self.interfaces:
            obj = Data(interface, data, manager)
            try:
                interface.validateInvariants(obj, errors)
            except Invalid:
                pass  # We continue to get a complete errors log.
        return errors
