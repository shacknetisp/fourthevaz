#For Beha's Servers
from base import *
import shelve
dbfile = "/home/server/.redeclipse/master.trunk/records";

def msg(mp):
  try:
    if mp.cmd("ranks"):
      if not mp.argsdef():
        print("No type specified!")
        return
      r=[]
      db = shelve.open(dbfile,'r')
      for i in db.keys():
        print(i)
        r.append([i,float(db[i])])
      db.close()
      r2 = []
      for i in sorted(r, key=lambda entry: entry[1]):
        if(mp.argsdef()=="fight" and i[0].find("_ratio")!=-1):
          r2.append(i[0].replace("_ratio","")+": "+str(i[1]))
      r2=list(reversed(r2))
      main.sendcmsg("Top player: "+r2[0])
      cmd.outlist(r2)
  except IndexError:
    main.sendcmsg("Cannot get data.")
  except:
    main.sendcmsg("Cannot get data.")
    
def showhelp():
  main.sendcmsg(".ranks <type>: Show ranks for <evaz> players with <type>.")
  main.sendcmsg("Type can be: fight")
