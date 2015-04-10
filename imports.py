# -*- coding: utf-8 -*-
import irc
import configs
import configs.module as module
import configs.match as match
import configs.mload as mload
import moduleregistry
import utils
import irc.utils
import version
moduleregistry.add_module(irc)
moduleregistry.add_module(match)
moduleregistry.add_module(utils)
moduleregistry.add_module(irc.utils)
moduleregistry.add_module(module)
moduleregistry.add_module(configs)
moduleregistry.add_module(mload)
moduleregistry.add_module(version)