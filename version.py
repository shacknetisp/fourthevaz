# -*- coding: utf-8 -*-
import platform
name = "Fourth Evaz"
version = (0, 1, 7)
source = "https://github.com/shacknetisp/fourthevaz"


def gitstr():
    try:
        return "%s" % (open('.git/refs/heads/master').read().strip()[0:10])
    except FileNotFoundError:
        return ""


def versionstr():
    return "%d.%d.%d%s" % (version[0], version[1], version[2],
        '-' + gitstr() if gitstr() else '')


def pythonversionstr():
    return '{t[0]}.{t[1]}.{t[2]}'.format(t=platform.python_version_tuple())


def systemversionstr():
    return platform.platform()