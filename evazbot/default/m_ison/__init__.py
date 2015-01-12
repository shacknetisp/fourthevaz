# -*- coding: utf-8 -*-

from base import *
import datetime
import calendar

redflare = mload('m_ison.redflare')

redflares = {
    'ison': 'http://redflare.ofthings.net'
}

replacements = []

##mconfig/ison.py
##lines of the following:
#redflares['ison2']="http://redflare.ofthings.net"
##this will cause the command .ison2 to use that url
#replacements = ['name1', 'name2']
exec(c_locs.mconfig("ison"))


def calcstats(k, v):
    now = datetime.datetime.utcnow()
    rf = redflare.redflare(v, replacements)
    statdb = c_vars.variablestore(c_locs.dbhome + '/ison.' + k + '.db')
    try:
        statdb.load()
    except:
        pass
    s = rf.get_stats()
    if 'times' not in statdb.data_dict:
        statdb.data_dict['times'] = 0
    statdb.data_dict['times'] += 1
    if str(now.month) not in statdb.data_dict:
        statdb.data_dict[str(now.month)] = {}
    if str(now.hour) not in statdb.data_dict[str(now.month)]:
        statdb.data_dict[str(now.month)][str(now.hour)] = {}
    if 'servers' not in statdb.data_dict[
        str(now.month)][str(now.hour)]:
        statdb.data_dict[str(now.month)][
            str(now.hour)]['servers'] = {}
    if 'players' not in statdb.data_dict[
        str(now.month)][str(now.hour)]:
        statdb.data_dict[str(now.month)][
            str(now.hour)]['players'] = {}
    for server in s.data:
        if server['desc'] not in statdb.data_dict[
            str(now.month)][str(now.hour)]['servers']:
            statdb.data_dict[str(now.month)][
                str(now.hour)]['servers'][server['desc']] = 0
        statdb.data_dict[str(now.month)][
                str(now.hour)]['servers'][
                    server['desc']] += len(server['players'])
    for player in s.players():
        if player not in statdb.data_dict[
            str(now.month)][str(now.hour)]['players']:
            statdb.data_dict[str(now.month)][
                str(now.hour)]['players'][player] = 0
        statdb.data_dict[str(now.month)][
                str(now.hour)]['players'][
                    player] += 1
    statdb.save()


def msg(mp):
    for k in list(redflares.keys()):
        v = redflares[k]
        if mp.wcmd(k):
            search = mp.args()
            rf = redflare.redflare(v, replacements)
            statdb = c_vars.variablestore(c_locs.dbhome + '/ison.' + k + '.db')
            try:
                statdb.load()
            except:
                pass
            if mp.argbool('stats'):
                s = rf.get_stats()
                out = []
                out.append('Servers: ' + str(len(rf.data)))
                out.append('Players: ' + str(s.numplayers()))
                out.append('Used Servers: ' + str(s.numservers()))
                cmd.outlist(out)
            elif mp.argbool('overall'):
                times = statdb.data_dict['times']
                allservers = {}
                allplayers = {}
                mtservers = {}
                htservers = {}
                for mon, monv in list(statdb.data_dict.items()):
                    if mon != 'times':
                        mservers = {}
                        for hou, houv in list(monv.items()):
                            hservers = {}
                            for serv, servv in list(houv['servers'].items()):
                                if serv not in allservers:
                                    allservers[serv] = 0
                                allservers[serv] += servv

                                if serv not in mservers:
                                    mservers[serv] = 0
                                mservers[serv] += servv

                                if serv not in hservers:
                                    hservers[serv] = 0
                                hservers[serv] += servv
                            for pl, plv in list(houv['players'].items()):
                                if serv not in allplayers:
                                    allplayers[pl] = 0
                                allplayers[pl] += plv
                            if hou not in htservers:
                                htservers[hou] = 0
                            for k, v in list(hservers.items()):
                                htservers[hou] += v
                        if mon not in mtservers:
                            mtservers[mon] = 0
                        for k, v in list(mservers.items()):
                            mtservers[mon] += v

                top = int(mp.argstr('top', '4'))
                if top > 10:
                    top = 10
                    main.sendcmsg('Top must be < 10.')
                if mp.argbool('months'):
                    sorted_months = sorted(
                        list(
                            mtservers.items()),
                            key=lambda k_v: (-k_v[1], k_v[0])[:4])
                    maxp = top
                    for p, n in sorted_months:
                        maxp -= 1
                        main.sendcmsg(
                            calendar.month_name[int(p)] + ': ' + str(
                                round(n / times, 1)))
                        if maxp <= 0:
                            break
                if mp.argbool('hours'):
                    sorted_hours = sorted(
                        list(
                            htservers.items()),
                            key=lambda k_v: (-k_v[1], k_v[0])[:4])
                    maxp = top
                    for p, n in sorted_hours:
                        maxp -= 1
                        main.sendcmsg(p + ' UTC: ' + str(round(n / times, 1)))
                        if maxp <= 0:
                            break
                if mp.argbool('players'):
                    sorted_players = sorted(
                        list(
                            allplayers.items()),
                            key=lambda k_v: (-k_v[1], k_v[0])[:4])
                    maxp = top
                    for p, n in sorted_players:
                        maxp -= 1
                        main.sendcmsg(p + ': ' + str(round(n / times, 1)))
                        if maxp <= 0:
                            break
                if mp.argbool('servers'):
                    sorted_servers = sorted(
                        list(
                            allservers.items()),
                            key=lambda k_v: (-k_v[1], k_v[0])[:4])
                    maxp = top
                    for p, n in sorted_servers:
                        maxp -= 1
                        main.sendcmsg(p + ': ' + str(round(n / times, 1)))
                        if maxp <= 0:
                            break
            elif mp.argbool('calc'):
                calcstats(k, v)
            else:
                o = rf.find_name(search)
                main.sendcmsg('Found ' + str(o.totaln) + ' in '
                              + str(o.totals) + ' server(s).')
                for k in o.out:
                    outfinal = k + ": "
                    for i in o.out[k]:
                        outfinal += i + '; '
                    main.sendcmsg(outfinal)
            return True
    return False

import time
lastcalc = 0


def tick():
    global lastcalc
    if time.time() - lastcalc > 60:
        for k in list(redflares.keys()):
            v = redflares[k]
            calcstats(k, v)
        lastcalc = time.time()


def showhelp(h):
    h("ison [-stats] [-overall] [-calc] <name>: Find players from a RedFlare.")
    main.sendcmsg('-overall: -top=<top> -months -hours -players -servers')
    main.sendcmsg("ison may be another command, list below:")
    for k in list(redflares.keys()):
        v = redflares[k]
        h(k + ": " + v)
