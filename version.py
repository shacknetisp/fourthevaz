# -*- coding: utf-8 -*-
import platform
name = "Fourth Evaz"
version = (0, 2, 4)
source = "https://github.com/shacknetisp/fourthevaz"
docs = "https://shacknetisp.github.io/fourthevaz-documentation"


def gitstr():
    """
    Get the git master commit ID.
    If not in a git repository, return an empty str.
    """
    try:
        return "%s" % (open('.git/refs/heads/master').read().strip()[0:10])
    except FileNotFoundError:
        return ""
    except IndexError:
        return ""


def versionstr():
    """Get the bot version."""
    return "%d.%d.%d%s" % (version[0], version[1], version[2],
        '-' + gitstr() if gitstr() else '')


def pythonversionstr():
    """Get the python version."""
    return '{t[0]}.{t[1]}.{t[2]}'.format(t=platform.python_version_tuple())


def systemversionstr():
    """Get the system type."""
    return platform.uname().system
