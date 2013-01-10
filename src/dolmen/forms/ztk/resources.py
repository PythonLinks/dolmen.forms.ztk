# -*- coding: utf-8 -*-

from fanstatic import Resource, Library
from zeam.jsontemplate import jsontemplate


DolmenFormsZTKLibrary = Library("dolmen.form.ztk", 'js')
collection_js = Resource(
    DolmenFormsZTKLibrary, 'collection.js', depends=[jsontemplate])
