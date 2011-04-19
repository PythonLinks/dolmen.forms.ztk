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

  >>> from infrae.testbrowser import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

Now acccess the edit form:

  >>> browser.open('http://localhost/comment/edit')
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

  >>> u'Modify your comment' in browser.contents
  True

  >>> titlefield = browser.getControl('Title')
  >>> titlefield
  <Control name='form.field.title' type='text'>
  >>> titlefield.value
  'dolmen.forms'

  >>> commentfield = browser.getControl('Comment')
  >>> commentfield
  <Control name='form.field.comment' type='textarea'>
  >>> commentfield.value
  'Is great'

  >>> namefield = browser.getControl('Name')
  >>> namefield
  <Control name='form.field.name' type='text'>
  >>> namefield.value
  ''

We can now edit the content, and so it get modified:

  >>> titlefield.value = 'dolmen.forms.ztk'
  >>> commentfield.value = 'Is far cooler than not ztk'
  >>> changebutton = browser.getControl('Change')
  >>> changebutton
  <SubmitControl name='form.action.change' type='submit'>

  >>> changebutton.click()
  >>> 'Modification saved' in browser.contents
  True


"""
