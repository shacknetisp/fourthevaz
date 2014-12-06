# -*- coding: utf-8 -*-
from base import *
import subprocess
reload(subprocess)
import sys
import evazbot.configs.wordai as wordai
reload(wordai)
import pickle
wordai.dbfile = c_locs.dbhome + "/replies.db.pkl"
wordai.load()

def msg(mp):
  if(mp.wcmd("c")):   
    main.sendcmsg(wordai.process(mp.args()))
    return True
  if mp.wcmd("cfix"):
    if not mp.argbool("w") or not mp.argbool("n"):
      main.sendcmsg("Invalid Arguments")
      return True
    w=mp.argstr("w").strip()
    n=mp.argstr("n").strip()
    try:
      wordai.replace(w,n)
      main.sendcmsg("Replaced '"+w+"' with '"+n+"'")
    except KeyError:
      main.sendcmsg("'"+w+"' is not in the database.")
    return True
  if mp.wcmd("cprint"):
    wordai.load()
    print(wordai.getdictstring())
    return True
  return False
def showhelp():
    main.sendcmsg(".c <text>: Process <text>.")
    main.sendcmsg(".cfix -w=<word> -n=<newword>: Rename a word.")