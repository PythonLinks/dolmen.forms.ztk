================
dolmen.forms.ztk
================

``dolmen.forms.ztk`` help you to integrate `dolmen.forms.base`_ with the
Zope Tool Kit. It provides:

- Form fields generation out of zope.schema fields, and zope.schema
  fields listed in a Zope interface,

- Widgets for those fields,

- Default action to Add, Edit a content, Cancel a current action by
  returning on the default view of a content.

Like `dolmen.forms.base`_ the focus is to have an API usable by the
developer, not a support of theorical use-cases that you don't need.

.. contents::

Example
=======

Let's create a form to edit a content. Here we have an interface for
our content::

  from zope import schema, interface

  class IClan(interface.Interface):
     pass

  class IPerson(interface.Interface):

     first_name = schema.TextLine(title=u"First Name")
     last_name = schema.TextLine(title=u"Last Name")
     age = schema.Int(title=u"Age", required=False)
     single = schema.Bool(title=u"Is single ?", default=True)

We assume that a Person is in a Clan. We can implement a Person::

  from persistence import Persistent

  class Person(Persistent):
      interface.implements(IPerson)

      first_name = None
      last_name = None
      age = None
      single = True


API
===

All the API of ``dolmen.forms.base`` is exported as well.

Fields
------

Currently supported fields:

- Date, Datetime: generate a text line input and parse/display the
  date using the locale,

- TextLine, Text, Boolean, URI, and numbers (Int, Float ...),

- Password,

- Choice: generate a select or a radio boxes (widget mode ``radio``),

- Object,

- Collections: List, Set, Tuple in input and display mode:

  - Collection of choices: generate a widget with a list of checkboxes,

  - Collection of objects: generate a table to edit multiple objects,

  - Other collection: generate a widget with generic add an remove actions.


For more documentation, please report to the doctests included in the code.


.. _dolmen.forms.base: http://pypi.python.org/pypi/dolmen.forms.base
