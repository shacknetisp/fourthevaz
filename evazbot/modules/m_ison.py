# -*- coding: utf-8 -*-
from base import *
import ast
from urllib.request import urlopen
import pprint

url="http://redflare.ofthings.net"

def msg(mp):
  if mp.wcmd("ison"):
    search = mp.args()
    found = {}
    with urlopen(url+"/reports") as u:
      servers = ast.literal_eval(u.read().decode())
      if mp.argbool("stats"):
        out = []
        out.append("Servers: "+str(len(servers)))
        total={
          'names':0,
          }
        for k in servers:
          v = servers[k]
          total['names']=total['names']+int(v['clients'])
        out.append("Players: "+str(total['names']))
        out.append(str(round(len(servers)/total['names'],1))+"x servers vs players.")
        cmd.outlist(out)
      else:
        total_names = 0
        total_servers = 0
        for server in servers.keys():
          for name_p in servers[server]['playerNames']:
            name = name_p['plain']
            if name.lower().find(search.lower()) != -1:
              if server not in found:
                found[server]=list()
              found[server].append(name)
              total_names = total_names+1
        main.sendcmsg("Found "+str(total_names)+" in "+str(len(found))+" server(s).")
        for s in found:
          out = servers[s]['description']+": "
          for p in found[s]:
            out+=p+"; "
          main.sendcmsg(out)
    return True
  return False
  
def showhelp():
  main.sendcmsg(".ison <name>: Search "+url+" for <name>.")
  main.sendcmsg(".ison -stats: Search "+url+" for server statistics.")