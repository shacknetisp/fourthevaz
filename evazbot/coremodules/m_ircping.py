# -*- coding: utf-8 -*-
from base import *


def ping(ct):
    main.ircwrite("PONG " + ct.text()[6:])
    print("Ping Processed.")