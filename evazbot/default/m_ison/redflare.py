# -*- coding: utf-8 -*-
from base import *
import ast
import urllib.request


class redflare:

    def __init__(self, url, replacements=[]):
        with urllib.request.urlopen(url + '/reports') as u:
            urldata = u.read().decode()
            for i in replacements:
                urldata = urldata.replace(i, cmd.getname(i, False))
            self.data = ast.literal_eval(urldata)

    class stats_out:

        def __init__(self, servers):
            self.data = servers

        def players(self):
            out = []
            for i in self.data:
                out += i['players']
            return out

        def numservers(self):
            return len(self.data)

        def numplayers(self):
            return len(self.players())

    def get_stats(self):
        out = []
        for k in self.data:
            v = self.data[k]
            pnames = []
            for i in v['playerNames']:
                pnames.append(i['plain'])
            if len(pnames) > 0:
                out.append({
                    'desc': v['description'],
                    'players': pnames,
                })
        return redflare.stats_out(out)

    class find_name_out:

        def __init__(self, totaln, totals, out):
            self.totaln = totaln
            self.totals = totals
            self.out = out

    def find_name(self, search):
        total_names = 0
        found = {}
        for server in list(self.data.keys()):
            for name_p in self.data[server]['playerNames']:
                name = name_p['plain']
                if name.lower().find(search.lower()) != -1:
                    if server not in found:
                        found[server] = list()
                    found[server].append(name)
                    total_names = total_names + 1
        outlist = {}
        for s in found:
            outnlist = []
            for p in found[s]:
                outnlist.append(p)
            outlist[self.data[s]['description']] = outnlist
        return redflare.find_name_out(total_names, len(found), outlist)
