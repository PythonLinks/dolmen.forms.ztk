# -*- coding: utf-8 -*-

from dolmen.forms.base.interfaces import IField
from dolmen.forms.base.widgets import FieldWidget
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.location import get_absolute_url
from grokcore import component as grok
from zope.interface import Interface


class LinkFieldWidget(FieldWidget):
    grok.adapts(IField, Interface, Interface)
    grok.name('link')

    template = getTemplate('linkfieldwidget.pt')

    def url(self):
        content = self.form.getContentData().getContent()
        return get_absolute_url(content, self.request)
