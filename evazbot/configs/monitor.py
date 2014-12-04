# -*- coding: utf-8 -*-
#Beha's Server SPECIFIC!!!
from base import *
import evazbot.configs.c_locs as c_locs
reload(c_locs)


def addline(line):
    with open(c_locs.rehome + "/ircbotcommands", "a") as myfile:
        myfile.write("\n" + line + "\n")
