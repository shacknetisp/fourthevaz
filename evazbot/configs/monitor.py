# -*- coding: utf-8 -*-
from base import *
import evazbot.configs.c_redeclipse as c_redeclipse
reload(c_redeclipse)


def addline(line):
    with open(c_redeclipse.rehome + "/ircbotcommands", "a") as myfile:
        myfile.write("\n" + line + "\n")
