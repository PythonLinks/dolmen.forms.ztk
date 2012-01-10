"""
We are going to define a simple form with an action and two fields
coming from a Zope interface.

We put our example in a separate file, since the configure.zcml of
dolmen.forms needs to be loaded in order to be able to create the fields,
which is no the case when the tests are collected.

Let's grok our example:

  >>> from dolmen.forms.ztk.testing import grok
  >>> grok('dolmen.forms.ztk.tests.integration.ztkform_fixture')

We can now lookup our form by the name of its class:

  >>> from cromlech.browser.testing import TestHTTPRequest
  >>> request = TestHTTPRequest()

  >>> from dolmen.forms.ztk.tests.integration.ztkform_fixture import Person
  >>> context = Person()
  >>> context.__name__ = 'person'

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='personform')
  >>> form
  <dolmen.forms.ztk.tests.integration.ztkform_fixture.PersonForm object at ...>

  >>> len(form.actions)
  1

  >>> print list(form.fields)
  [<TextLineSchemaField Person name>, <IntSchemaField Person age>]


Integration test
----------------

Let's try to take a browser and submit that form:

  >>> root = getRootFolder()
  >>> context.__parent__ = root
  >>> app = makeApplication(context, 'personform')

  >>> from infrae.testbrowser.browser import Browser
  >>> browser = Browser(app)
  >>> browser.options.handle_errors = False
  >>> browser.handleErrors = False

We can access the form, fill it and submit it:

  >>> browser.open('http://localhost/person/personform')
  200
  >>> form = browser.get_form(id='form')
  >>> namefield = form.get_control('form.field.name')
  >>> namefield.name, namefield.type
  ('form.field.name', 'text')
  >>> namefield.value = 'Arthur Sanderman'

  >>> agefield = form.get_control('form.field.age')
  >>> agefield.name, agefield.type
  ('form.field.age', 'text')
  >>> agefield.value = '42'

  >>> form.get_control('form.action.send').click()
  200

  >>> 'We sent Arthur Sanderman, age 42' in browser.contents
  True

"""
