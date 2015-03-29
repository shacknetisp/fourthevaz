# -*- coding: utf-8 -*-
import platform
name = "Fourth Evaz"
version = (0, 9, 0)
source = "https://github.com/shacknetisp/fourthevaz"


def versionstr():
    return "%d.%d.%d" % (version[0], version[1], version[2])


def pythonversionstr():
    return '{t[0]}.{t[1]}.{t[2]}'.format(t=platform.python_version_tuple())


def systemversionstr():
    return platform.platform()