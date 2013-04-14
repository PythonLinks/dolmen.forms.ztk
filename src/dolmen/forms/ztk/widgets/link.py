# -*- coding: utf-8 -*-

import crom
from dolmen.forms.base.interfaces import IField, IWidget
from dolmen.forms.base.widgets import FieldWidget
from dolmen.forms.ztk.widgets import getTemplate
from zope.interface import Interface


@crom.adapter
@crom.name('link')
@crom.target(IWidget)
@crom.sources(IField, Interface, Interface)
class LinkFieldWidget(FieldWidget):

    template = getTemplate('linkfieldwidget.pt')

    def url(self):
        content = self.form.getContentData().getContent()
        return IURL(content, self.request)
