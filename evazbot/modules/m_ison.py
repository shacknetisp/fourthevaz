# -*- coding: utf-8 -*-

from base import *
import ast
from urllib.request import urlopen

url = 'http://redflare.ofthings.net'


def msg(mp):
    if mp.wcmd('ison'):
        search = mp.args()
        found = {}
        with urlopen(url + '/reports') as u:
            urldata = u.read().decode()
            if hasattr(c_wlist, "replacements"):
                for i in c_wlist.replacements:
                    urldata = urldata.replace(i, cmd.getname(i, False))
            servers = ast.literal_eval(urldata)
            if mp.argbool('stats'):
                out = []
                out.append('Servers: ' + str(len(servers)))
                total = {'names': 0, 'servers': 0}
                for k in servers:
                    v = servers[k]
                    total['names'] = total['names'] + int(v['clients'])
                    if int(v['clients']) > 0:
                        total['servers'] = total['servers'] + 1
                out.append('Players: ' + str(total['names']))
                if total['names'] > 0:
                    out.append(str(round(len(servers) / total['names'], 1))
                        + 'x servers vs players.')
                out.append('Used Servers: ' + str(total['servers']))
                cmd.outlist(out)
            else:
                total_names = 0
                for server in list(servers.keys()):
                    for name_p in servers[server]['playerNames']:
                        name = name_p['plain']
                        if name.lower().find(search.lower()) != -1:
                            if server not in found:
                                found[server] = list()
                            found[server].append(name)
                            total_names = total_names + 1
                main.sendcmsg('Found ' + str(total_names) + ' in '
                              + str(len(found)) + ' server(s).')
                for s in found:
                    out = servers[s]['description'] + ': '
                    for p in found[s]:
                        out += p + '; '
                    main.sendcmsg(out)
        return True
    return False


def showhelp():
    main.sendcmsg('.ison <name>: Search ' + url + ' for <name>.')
    main.sendcmsg('.ison -stats: Search ' + url
                  + ' for server statistics.')
