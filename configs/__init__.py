# -*- coding: utf-8 -*-
import moduleregistry
from . import locs as locs
moduleregistry.add_module(locs)
from . import servers as servers
moduleregistry.add_module(servers)