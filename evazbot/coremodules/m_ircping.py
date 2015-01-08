# -*- coding: utf-8 -*-
from base import *


def ping(mp):
    main.ircwrite("PONG " + mp.text()[6:])
    print("Ping Processed.")