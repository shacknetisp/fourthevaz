# -*- coding: utf-8 -*-
from base import *


def ping():
    main.ircwrite("PONG :pingis")
    print("Ping Processed.")