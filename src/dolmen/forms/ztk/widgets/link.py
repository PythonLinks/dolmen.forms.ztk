# -*- coding: utf-8 -*-

from dolmen.forms.base.interfaces import IField
from dolmen.forms.base.widgets import FieldWidget
from dolmen.forms.ztk.widgets import getTemplate

from zope.component import getMultiAdapter
from zope.interface import Interface
from cromlech.browser.interfaces import IURLResolver

from grokcore import component as grok


class LinkFieldWidget(FieldWidget):
    grok.adapts(IField, Interface, Interface)
    grok.name('link')

    template = getTemplate('linkfieldwidget.pt')

    def url(self):
        return str(getMultiAdapter(
            (self.form.context, self.request), IURLResolver))
