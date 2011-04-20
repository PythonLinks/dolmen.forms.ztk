"""
We are going to use a simple form with an edit action to edit a comment.

Let's grok our example:

  >>> from dolmen.forms.ztk.testing import grok
  >>> grok('dolmen.forms.ztk.tests.integration.editform_fixture')

Let's add a comment and try to edit it with our form:

  >>> from dolmen.forms.ztk.tests.integration.editform_fixture import Comment
  >>> root = getRootFolder()
  >>> comment = Comment(u'dolmen.forms', u'Is great')
  >>> comment.__name__ = 'comment'
  >>> comment.__parent__ = root
  
  >>> comment.title
  u'dolmen.forms'
  >>> comment.comment
  u'Is great'

  >>> from infrae.testbrowser.browser import Browser
  >>> edit = makeApplication(comment, 'edit')
  
  >>> browser = Browser(edit)
  >>> browser.handleErrors = False

Now acccess the edit form:

  >>> browser.open('http://localhost/comment/edit')
  200
  >>> browser.set_request_header('Authorization', 'Basic mgr:mgrpw')

  >>> u'Modify your comment' in browser.contents
  True

  >>> form = browser.get_form(id='form')
  >>> titlefield = form.get_control('form.field.title')
  >>> titlefield.name, titlefield.type
  ('form.field.title', 'text')
  >>> titlefield.value
  'dolmen.forms'

  >>> commentfield = form.get_control('form.field.comment')
  >>> commentfield.name, commentfield.type
  ('form.field.comment', 'textarea')
  >>> commentfield.value
  'Is great'

  >>> namefield = form.get_control('form.field.name')
  >>> namefield.name, namefield.type
  ('form.field.name', 'text')
  >>> namefield.value
  ''

We can now edit the content, and so it get modified:

  >>> titlefield.value = 'dolmen.forms.ztk'
  >>> commentfield.value = 'Is far cooler than not ztk'
  >>> changebutton = form.get_control('form.action.change')
  >>> changebutton.name, changebutton.type
  ('form.action.change', 'submit')

  >>> changebutton.click()
  200
  >>> 'Modification saved' in browser.contents
  True


"""
