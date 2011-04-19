# -*- coding: utf-8 -*-

from grokcore.component import zcml
from zope.configuration.config import ConfigurationMachine


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('dolmen.view.meta', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()
