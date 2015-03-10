# -*- coding: utf-8 -*-
import ast
from . import locs
import moduleregistry
moduleregistry.add_module(locs)
serverscfg = locs.userdata + '/servers.py'
try:
    servers = ast.literal_eval(open(serverscfg).read())
except FileNotFoundError:
    raise FileNotFoundError(
        'Look at examples/servers.py to set up your IRC configuration.' +
        ' %s was not found.' % serverscfg)