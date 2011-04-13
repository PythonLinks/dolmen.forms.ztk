# this is a package.

import os.path
from dolmen.template import TALTemplate

TEMPLATES = os.path.join(os.path.dirname(__file__), 'templates')

def getTemplate(path):
    return TALTemplate(os.path.join(TEMPLATES, path))
