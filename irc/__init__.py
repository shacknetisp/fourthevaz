# -*- coding: utf-8 -*-
import moduleregistry
from . import server as server
moduleregistry.add_module(server)
from . import utils as utils
moduleregistry.add_module(utils)