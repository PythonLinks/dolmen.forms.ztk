# -*- coding: utf-8 -*-

import grokcore.component as grok

from cromlech.webob.response import Response
from dolmen.forms.base import Fields, Actions, Form
from dolmen.forms.ztk import EditAction
from zope import interface, schema


class IComment(interface.Interface):

    title = schema.TextLine(
        title=u"Title",
        required=True)

    comment = schema.Text(
        title=u"Comment",
        required=True)

    name = schema.TextLine(
        title=u"Name",
        required=False)


class Comment(grok.Context):
    grok.implements(IComment)

    def __init__(self, title, comment, name=''):
        self.title = title
        self.comment = comment
        self.name = name


class Edit(Form):
    """An edit form.
    """
    responseFactory = Response

    label = u"Modify your comment"
    ignoreContent = False

    fields = Fields(IComment)
    actions = Actions(EditAction(u"Change"))


from zope.security.protectclass import protectName, protectSetAttribute
# Need to declare security for Zope madness

protectName(Comment, 'title', 'zope.Public')
protectName(Comment, 'comment', 'zope.Public')
protectName(Comment, 'name', 'zope.Public')

# Everybody as edit right, so test are simpler
protectSetAttribute(Comment, 'title', 'zope.Public')
protectSetAttribute(Comment, 'comment', 'zope.Public')
protectSetAttribute(Comment, 'name', 'zope.Public')
