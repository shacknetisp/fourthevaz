# -*- coding: utf-8 -*-
from importlib import reload
registry = []
reloadscheduled = False


def delete_module(m):
    """Delete a module from the reloading registry."""
    global registry
    registry = list(filter((m).__ne__, registry))


def add_module(m):
    """Add a python module to the reloading registry."""
    global registry
    if m in registry:
        return
    registry.append(m)
    if hasattr(m, '__noreload') and m.__noreload:
        return
    reload(m)


def reload_all():
    """Reload all modules in the registry."""
    global registry
    for m in registry:
        if hasattr(m, '__noreload') and m.__noreload:
            continue
        reload(m)