# -*- coding: utf-8 -*-

from base import *
import datetime
import calendar
import re
import time

redflare = mload('m_ison.redflare')

redflares = {
    'ison': 'http://redflare.ofthings.net'
}

replacements = []

overallround = 2

##mconfig/ison.py
##lines of the following:
##this will cause the command .ison2 to use that url
#redflares['ison2']="http://redflare.ofthings.net"
##replace in the .ison
#replacements = ['name1', 'name2']
##round for -overall
#overallround = 2
exec(c_locs.mconfig("ison"))


def start():
    return list(redflares.keys())


def calcstats(k, v):
    now = datetime.datetime.utcnow()
    rf = redflare.redflare(v, replacements)
    statdb = c_vars.liststore(c_locs.dbhome + '/ison.' + k + '.db')
    try:
        statdb.load()
    except:
        pass
    s = rf.get_stats()
    deletionlist = []
    for dk in range(len(statdb.data_list)):
        try:
            if (time.time() - statdb.data_list[dk]['timestamp'] >
            (60 * 60 * 24 * 8)):
                    deletionlist.append(dk)
        except KeyError:
            deletionlist.append(dk)
    print('Deleting %d from stat table.' % len(deletionlist))
    for tod in deletionlist:
        del statdb.data_list[tod]
    outd = {'timestamp': time.time(), 'dictionary': {}}
    ddnum = outd['dictionary']
    if str(now.weekday()) not in ddnum:
        ddnum[str(now.weekday())] = {}
    if str(now.hour) not in ddnum[str(now.weekday())]:
        ddnum[str(now.weekday())][str(now.hour)] = {}
    if 'servers' not in ddnum[
        str(now.weekday())][str(now.hour)]:
        ddnum[str(now.weekday())][
            str(now.hour)]['servers'] = {}
    if 'players' not in ddnum[
        str(now.weekday())][str(now.hour)]:
        ddnum[str(now.weekday())][
            str(now.hour)]['players'] = {}
    for server in s.data:
        if server['desc'] not in ddnum[
            str(now.weekday())][str(now.hour)]['servers']:
            ddnum[str(now.weekday())][
                str(now.hour)]['servers'][server['desc']] = 0
        ddnum[str(now.weekday())][
                str(now.hour)]['servers'][
                    server['desc']] += len(server['players'])
    for player in s.players():
        if player not in ddnum[
            str(now.weekday())][str(now.hour)]['players']:
            ddnum[str(now.weekday())][
                str(now.hour)]['players'][player] = 0
        ddnum[str(now.weekday())][
                str(now.hour)]['players'][
                    player] += 1
    statdb.data_list.append(outd)
    print("Calculated statistics.")
    statdb.save()


allservers = {}
allplayers = {}
mtservers = {}
htservers = {}


def calcoverall(k, v):
    statdb = c_vars.liststore(c_locs.dbhome + '/ison.' + k + '.db')
    try:
        statdb.load()
    except:
        pass
    global allservers
    global allplayers
    global mtservers
    global htserver
    allservers[k] = {}
    allplayers[k] = {}
    mtservers[k] = {}
    htservers[k] = {}
    for dli in statdb.data_list:
        ddnum = dli['dictionary']
        for mon, monv in list(ddnum.items()):
            mservers = {}
            for hou, houv in list(monv.items()):
                hservers = {}
                for serv, servv in list(houv['servers'].items()):
                    if serv not in allservers[k]:
                        allservers[k][serv] = 0
                    allservers[k][serv] += servv

                    if serv not in mservers:
                        mservers[serv] = 0
                    mservers[serv] += servv

                    if serv not in hservers:
                        hservers[serv] = 0
                    hservers[serv] += servv
                for pl, plv in list(houv['players'].items()):
                    if pl.lower() not in allplayers[k]:
                        allplayers[k][pl.lower()] = 0
                    allplayers[k][pl.lower()] += plv
                if hou not in htservers[k]:
                    htservers[k][hou] = 0
                for hk, hv in list(hservers.items()):
                    htservers[k][hou] += hv
            if mon not in mtservers[k]:
                mtservers[k][mon] = 0
            for mk, mv in list(mservers.items()):
                mtservers[k][mon] += mv
    print("Calculated overall.")


def getoverall(mp, k, v, statdb):
    global allservers
    global allplayers
    global mtservers
    global htserver
    outall = ['Results']
    try:
        top = int(mp.argstr('top', '4'))
    except ValueError:
        top = 4
    if top > 10:
        top = 10
        main.sendcmsg('Top must be <= 10.')
    gotarg = False
    if mp.argbool('days'):
        gotarg = True
        sorted_months = sorted(
            list(
                mtservers[k].items()),
                key=lambda k_v: (-k_v[1], k_v[0]))
        maxp = top
        index = 0
        for p, n in sorted_months:
            index += 1
            if calendar.day_name[
                  int(p)].lower() == mp.argsdef().lower() or len(
                      mp.argsdef().lower()) == 0:
                maxp -= 1
                if maxp > 0:
                    outall.append(
                        calendar.day_name[int(p)] + ': ' + str(
                            round(n / sorted_months[0][1], overallround))
                            + " (" + str(index) + ")")
    if mp.argbool('hours'):
        gotarg = True
        sorted_hours = sorted(
            list(
                htservers[k].items()),
                key=lambda k_v: (-k_v[1], k_v[0]))
        maxp = top
        index = 0
        for p, n in sorted_hours:
            index += 1
            if p.lower() == mp.argsdef().lower() or len(
                  mp.argsdef().lower()) == 0:
                maxp -= 1
                if maxp >= 0:
                    outall.append(p + ' UTC: ' + str(
                        round(n / sorted_hours[0][1], overallround))
                        + " (" + str(index) + ")")
    if mp.argbool('players'):
        gotarg = True
        sorted_players = sorted(
            list(
                allplayers[k].items()),
                key=lambda k_v: (-k_v[1], k_v[0]))
        maxp = top
        index = 0
        for p, n in sorted_players:
            index += 1
            if (p.lower().find(mp.argsdef().lower()) != -1 or
            c_regex.contains(mp.argsdef(). lower(), p.lower())):
                maxp -= 1
                if maxp >= 0:
                    outall.append(p + ': ' + str(
                        round(n / sorted_players[0][1], overallround))
                        + " (" + str(index) + ")")
    if mp.argbool('servers'):
        gotarg = True
        sorted_servers = sorted(
            list(
                allservers[k].items()),
                key=lambda k_v: (-k_v[1], k_v[0]))
        maxp = top
        index = 0
        for p, n in sorted_servers:
            index += 1
            if (p.lower().find(mp.argsdef().lower()) != -1 or
            c_regex.contains(mp.argsdef(). lower(), p.lower())):
                maxp -= 1
                if maxp >= 0:
                    outall.append(p + ': ' + str(
                        round(n / sorted_servers[0][1], overallround))
                        + " (" + str(index) + ")")
    if not gotarg:
        outall.append('No useful options!')
    return outall


def msg(mp):
    for k in list(redflares.keys()):
        v = redflares[k]
        if mp.wcmd(k):
            search = mp.args()
            rf = redflare.redflare(v, replacements)
            statdb = c_vars.liststore(c_locs.dbhome + '/ison.' + k + '.db')
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
                try:
                    outall = getoverall(mp, k, v, statdb)
                    cmd.outlist(outall, 6, ', ')
                except re.error as e:
                    main.sendcmsg('Error: ' + str(e))
            elif mp.argbool('calc') and mp.isadmin(99):
                calcstats(k, v)
                calcoverall(k, v)
                main.sendcmsg('Calculated.')
            else:
                try:
                    o = rf.find_name(search)
                    main.sendcmsg('Found ' + str(o.totaln) + ' in '
                                  + str(o.totals) + ' server(s).')
                    for k in o.out:
                        outfinal = k + ": "
                        for i in o.out[k]:
                            outfinal += i + '; '
                        main.sendcmsg(outfinal)
                except re.error as e:
                    main.sendcmsg('Error: ' + str(e))
            return True
    return False

lastcalc = 0
lastcalc2 = 0


def tick():
    global lastcalc
    if time.time() - lastcalc > 60 * 6:
        for k in list(redflares.keys()):
            v = redflares[k]
            calcstats(k, v)
        lastcalc = time.time()
    global lastcalc2
    if time.time() - lastcalc2 > 60 * 12:
        for k in list(redflares.keys()):
            v = redflares[k]
            calcoverall(k, v)
        lastcalc2 = time.time()


def showhelp(h):
    h("ison [-stats] [-overall] [-calc] <name>: Find players from a RedFlare.")
    main.sendcmsg(
        '-overall: -top=<top> -days -hours -players -servers ["search"]')
    main.sendcmsg("ison may be another command, list below:")
    for k in list(redflares.keys()):
        v = redflares[k]
        h(k + ": " + v)
