# -*- coding: utf-8 -*-
from base import *
import subprocess
reload(subprocess)
import sys
from pprint import pprint
from random import choice
import random
import string
import pickle

dbfile = c_locs.dbhome + "/replies.db.pkl"

data_dict = {}
 
def ms(r):
    exclude = set(string.punctuation)
    r = ''.join(ch for ch in r if ch not in exclude)
    inp = r.lower().split()
    if len(inp):
      if not ';start' in data_dict:
        data_dict[';start']=list()
      if not ';end' in data_dict:
        data_dict[';end']=list()
      if not inp[0] in data_dict[';start'] or True:
        data_dict[';start'].append(inp[0])
      if not inp[-1] in data_dict[';end'] or True:
        data_dict[';end'].append(inp[-1])
    for i in range(len(inp)):
      if not inp[i] in data_dict:
        data_dict[inp[i]]=list()
      try:
        if not inp[i+1] in data_dict[inp[i]] or True:
          data_dict[inp[i]].append(inp[i+1])
      except IndexError:
        pass
    ret = ""
    try:
      if random.randrange(0,100) < 30:
        first = choice(inp)
      elif random.randrange(0,100) < 60:
        first = inp[0]
      else:
        first = inp[-1]
      if not first in data_dict[';start'] or random.randrange(0,100) < 40:
        first = choice(data_dict[';start'])
      ret+=first+" ";
      nextword = first
      for numwords in range(100):
        if nextword in data_dict:
          cnext = choice(data_dict[nextword])
          ret+=cnext+" "
          if nextword in data_dict[';end'] and random.randrange(0,100) < 50:
            break
          nextword=cnext
        else:
          break
    except IndexError:
      pass
    except KeyError:
      pass
    try:
      return str(str(ret[0]).upper()+ret[1:]).strip()+"."
    except IndexError:
      return "?"
def msg(mp):
  global data_dict
  if(mp.cmd("c")):
    try:
      dict_file = open(dbfile, 'rb')           
      data_dict = pickle.load(dict_file)
      dict_file.close()
    except FileNotFoundError:
      pass
    except IOError:
      pass
    except EOFError:
      pass
    
    main.sendcmsg(ms(mp.args()))
    
    output = open(dbfile, 'wb')
    pickle.dump(data_dict, output)
    output.close()
    return True
  if mp.cmd("cfix"):
    if not mp.argbool("w") or not mp.argbool("n"):
      main.sendcmsg("Invalid Arguments")
      return True
    w=mp.argstr("w").strip()
    n=mp.argstr("n").strip()
    if n!=w:
     data_dict[n] = data_dict[w]
     del data_dict[w]
    for k in data_dict:
     for index, item in enumerate(data_dict[k]):
      if item==w:
       data_dict[k][index] = n
    output = open(dbfile, 'wb')
    pickle.dump(data_dict, output)
    output.close()
    return True
  if mp.cmd("cprint"):
    try:
      dict_file = open(dbfile, 'rb')           
      data_dict = pickle.load(dict_file)
      dict_file.close()
    except FileNotFoundError:
      pass
    except IOError:
      pass
    except EOFError:
      pass
    pprint(data_dict)
    return True
  return False
def showhelp():
    main.sendcmsg(".c <text>: Process <text>.")
    main.sendcmsg(".cfix -w=<word> -n=<newword>: Rename a word.")