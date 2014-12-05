# -*- coding: utf-8 -*-
import sys
from imp import reload
import inspect
import importlib
import evazbot.main as main
import traceback
import evazbot.configs.c_locs as c_locs

reload(c_locs)

sys.path.append(c_locs.dbhome+"/modules")
dbfile = c_locs.dbhome + "/defaultmodules.db.txt"
custom_offset = 2
offset = 1
name_offset = 0

def unique(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def needmodule(n):
  global modules
  modules.append(n)

def init():
    global module_callbacks
    global modules
    # Format: Name, Module
    module_callbacks = []
    modules = []
    try:
      for line in open(dbfile, "r"):
        if len(line.strip()) > 0:
            modules.append(line.strip())
    except FileNotFoundError:
      modules.append("core")
    needmodule("core")
    needmodule("ircping")
    needmodule("help")
    modules = unique(modules)


def helpmodulenames():
    ret = []
    for i in module_callbacks:
        if hasattr(i[offset], "showhelp"):
            ret.append(i[name_offset])
    return ret


def incomplete(i):
    return


def add(i):
    i = i.strip()
    custom = False
    try:
        newmodule = importlib.import_module("evazbot.modules.m_" + i)
    except ImportError:
        try:
            newmodule = importlib.import_module("evazbot.modules.custom.mc_" + i)
            custom = True
        except ImportError as e:
            try:
              newmodule = importlib.import_module("mp_" + i)
              custom = True
            except ImportError as e:
              main.sendcmsg("Cannot import module!");
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
            main.sendcmsg("Module " + n + " has been removed.")
            del module_callbacks[i]
            return True
    return False


def astart(n):
    n = n.strip()
    remove(n)
    newmodule = add(n)
    try:
        newmodule.start()
    except AttributeError:
            incomplete(n)
    except NameError:
            incomplete(n)
    main.sendcmsg("Module " + n + " has been added.")


def load():
    errorcount = 0
    for i in modules:
        try:
            add(i)
        except ImportError:
            traceback.print_exc()
            errorcount += 1
    print(str(errorcount) + " error(s) while loading!")


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


def event(f, s=""):
    import evazbot.configs.u_commands as cmd

    reload(cmd)
    for i in module_callbacks:
        try:
            function = getattr(i[offset], f)
            asp = inspect.getargspec(function)
            if len(asp.args) == 1:
                function(cmd.MParser(s))
            else:
                function()
        except AttributeError:
            incomplete(i[name_offset])
        except:
            traceback.print_exc()


def showhelp(n):
    n = n.strip()
    for i in module_callbacks:
        if i[name_offset] == n:
            try:
                i[offset].showhelp()
            except AttributeError:
                incomplete(n)
                main.sendcmsg(n+" is not interactive.")
            except:
                traceback.print_exc()
