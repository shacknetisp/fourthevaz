# -*- coding: utf-8 -*-
import sys
from imp import reload
import inspect
import importlib
import evazbot.main as main
import traceback
import evazbot.configs.c_locs as c_locs

reload(c_locs)

sys.path.append(c_locs.dbhome + "/modules")
dbfile = c_locs.dbhome + "/automodules." + main.moduleset + ".db.txt"
custom_offset = 2
offset = 1
name_offset = 0
modules = []
module_callbacks = []
module_registry = {}


def unique(seq, idfun=None):
    if idfun is None:
        def idfun(x):
            return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def needmodule(n):
    global modules
    modules.append(n)


def init():
    import evazbot.coremodules.c_corelist as corelist
    global module_callbacks
    global modules
    # Format: Name, Module
    module_callbacks = []
    modules = []
    for i in corelist.needed:
        needmodule(i)
    try:
        for line in open(dbfile, "r"):
            if len(line.strip()) > 0:
                modules.append(line.strip())
    except IOError:
        modules.append("core")
    modules = unique(modules)


def helpmodulenames():
    ret = []
    for i in module_callbacks:
        if hasattr(i[offset], "showhelp"):
            ret.append(i[name_offset])
    return ret


def incomplete(i=''):
    return


def add(i):
    i = i.strip()
    custom = False
    try:
        newmodule = importlib.import_module("mp_" + i)
        custom = True
    except ImportError as e:
        try:
            newmodule = importlib.import_module(
                "evazbot." + main.moduleset + ".m_" + i)
        except ImportError as e:
            try:
                newmodule = importlib.import_module(
                    "evazbot.coremodules.m_" + i)
            except ImportError as e:
                main.sendcmsg("Cannot import module!")
                raise e
    reload(newmodule)
    module_callbacks.append((i, newmodule, custom))
    return newmodule


def remove(n):
    n = n.strip()
    for i in range(len(module_callbacks)):
        if module_callbacks[i][name_offset] == n:
            try:
                module_callbacks[i][offset].stop()
            except AttributeError:
                incomplete(n)
            except NameError:
                incomplete(n)
            try:
                print(("Removing module registry: " + str(module_registry[n])))
                del module_registry[n]
            except KeyError:
                pass
            del module_callbacks[i]
            return True
    return False


def astart(n):
    n = n.strip()
    remove(n)
    newmodule = add(n)
    global module_registry
    try:
        module_registry[n] = newmodule.start()
        print(("Adding module registry: " + str(module_registry[n])))
    except AttributeError:
            incomplete(n)
    except NameError:
            incomplete(n)
    return True


def load():
    errorcount = 0
    for i in modules:
        try:
            astart(i)
        except ImportError:
            traceback.print_exc()
            errorcount += 1
    print((str(errorcount) + " error(s) while loading!"))


def reloadall():
    for i in range(len(module_callbacks)):
        try:
            module_callbacks[i][offset].stop()
        except AttributeError:
                        incomplete(module_callbacks[i][name_offset])
        except NameError:
                        incomplete(module_callbacks[i][name_offset])
    # del module_callbacks
    main.sendcmsg("Removed all modules.")
    init()
    load()
    main.sendcmsg("Reloaded modules.")


def isget(f):
    return f == 'msg' or f == 'afterall' or f == 'get' or f == 'getafter'


def doevent(i, f, s):
    import evazbot.configs.u_commands as cmd
    import evazbot.irc as irc
    try:
        try:
            function = getattr(i[offset], f)
        except AttributeError:
            return
        asp = inspect.getargspec(function)
        mp = cmd.MParser(s)
        if len(asp.args) == 1 and (f == 'msg' or f == 'afterall'):
            function(mp)
        elif len(asp.args) == 1 and (f == 'get' or
        f == 'getafter' or
        f == 'ping'):
            function(irc.getcontext(mp))
        elif len(asp.args) == 2:
            function(mp, irc.getcontext(mp))
        else:
            function()
    except Exception as e:
        if isget(f):
            main.sendcmsg('Unhandled exception!')
            if cmd.isadmin(s) and cmd.iswlist(s):
                main.sendmsg(cmd.getircuser(s), str(e))
        traceback.print_exc()


def event(f, s=""):
    import evazbot.configs.u_commands as cmd
    if isget(f):
        modulewant = ''
        for k, v in list(module_registry.items()):
            if v is not None:
                for fc in v:
                    if cmd.getcmd(s, fc):
                        modulewant = k
        if len(modulewant) > 0:
            for r in range(len(module_callbacks)):
                if module_callbacks[r][name_offset] == modulewant:
                    doevent(module_callbacks[r], f, s)
                    return
    for i in module_callbacks:
        doevent(i, f, s)
    return


def showhelp(n):
    n = n.strip()
    found = False
    for i in module_callbacks:
        if i[name_offset] == n:
            try:
                function = getattr(i[offset], 'showhelp')
                asp = inspect.getargspec(function)
                if len(asp.args) == 0:
                    i[offset].showhelp()
                else:
                    i[offset].showhelp(main.sendhmsg)
            except AttributeError:
                incomplete(n)
                main.sendcmsg(n + " is not interactive.")
            except:
                traceback.print_exc()
            found = True
    if not found:
        main.sendcmsg(n + " does not exist.")
