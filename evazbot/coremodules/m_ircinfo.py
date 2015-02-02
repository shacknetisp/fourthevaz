# -*- coding: utf-8 -*-
from base import *


def start():
    return ["names", "whois"]


def get(ct):
    if ct.cmd('names'):
        channel = ct.args.getdef()
        if len(channel) == 0:
            channel = ct.channel()
            if ct.isprivate():
                ct.msg('You must specify a channel if run from a query.')
                return True
        if channel in main.ircprofiles[main.currentprofile]['channelnames']:
            out = []
            for i in main.ircprofiles[
                main.currentprofile]['channelnames'][channel]:
                    out.append(cmd.getname(i, False))
            ct.msg('%d names in %s:' % (len(out), channel))
            cmd.outlist(out)
        else:
            ct.msg('Cannot find channel.')
    elif ct.cmd("whois"):
        name = ct.args.getdef()
        if name not in main.ircprofiles[main.currentprofile]['userinfo']:
            ct.msg('Unable to find user.')
            return True
        was = False
        if main.ircprofiles[main.currentprofile]['userinfo'][name]['offline']:
            was = True
        u = main.ircprofiles[main.currentprofile]['userinfo'][name]
        ct.msg('%s%s: %s %s %s' % (
            name,
            " <offline>" if was else " <away>" if u['away'] else "",
            u['ident'],
            u['address'],
            u['name'],
            ))
        return True
    elif ct.code('311'):
        user = ct.getsplit(3)
        print(('Adding %s to userinfo list' % user))
        main.ircprofiles[main.currentprofile]['userinfo'][user] = {}
        main.ircprofiles[main.currentprofile]['userinfo'][user][
            'offline'] = False
        main.ircprofiles[main.currentprofile]['userinfo'][user][
            'away'] = False
        main.ircprofiles[main.currentprofile][
            'userinfo'][user]['ident'] = ct.getsplit(4)
        main.ircprofiles[main.currentprofile][
            'userinfo'][user]['address'] = ct.getsplit(5)
        main.ircprofiles[main.currentprofile][
            'userinfo'][user]['name'] = ct.text()[ct.text().rfind(':') + 1:]
    elif ct.code('301'):
        user = ct.getsplit(3)
        main.ircprofiles[main.currentprofile]['userinfo'][user][
            'away'] = True
    elif ct.code("353"):
        ch = ct.getsplit(4)
        if ch not in main.ircprofiles[main.currentprofile]['channelnames']:
            main.ircprofiles[main.currentprofile]['channelnames'][ch] = []
        for i in ct.nameslist():
            n = i.strip('@+:')
            main.ircprofiles[main.currentprofile]['channelnames'][ch].append(
                n)
            main.ircprofiles[main.currentprofile]['whoisqueue'].append(n)
        main.ircprofiles[main.currentprofile][
            'channelnames'][ch] = c_utils.unique(
                main.ircprofiles[main.currentprofile]['channelnames'][ch])
        return True
    return False


def tick_profile():
    counter = 999
    if 'userinfo.counter' in main.ircprofiles[main.currentprofile]:
        counter = main.ircprofiles[main.currentprofile]['userinfo.counter']
    counter += 1
    counterdlist = 999
    if 'userinfo.counterdlist' in main.ircprofiles[main.currentprofile]:
        counterdlist = main.ircprofiles[
           main.currentprofile]['userinfo.counterdlist']
    counterdlist += 1
    if counterdlist > 10:
        dlist = []
        for search in main.ircprofiles[main.currentprofile]['userinfo']:
            found = False
            for channel in main.ircprofiles[main.currentprofile]['channels']:
                for i in main.ircprofiles[
                    main.currentprofile]['channelnames'][channel]:
                        if i == search:
                            found = True
            if not found:
                dlist.append(search)
        for i in dlist:
            main.ircprofiles[
                main.currentprofile]['userinfo'][i]['offline'] = True
        counterdlist = 0
    if counter > 120:
        for channel in main.ircprofiles[main.currentprofile]['channels']:
            if channel in main.ircprofiles[
                main.currentprofile]['channelnames']:
                main.ircprofiles[
                    main.currentprofile]['channelnames'][channel] = []
            print(('Updating names list for %s' % channel))
            main.ircwrite("NAMES %s" % channel)
        counter = 0
    main.ircprofiles[main.currentprofile]['userinfo.counter'] = counter
    main.ircprofiles[main.currentprofile][
        'userinfo.counterdlist'] = counterdlist


def showhelp(h):
    h('names [<channel>]: Get IRC names list.')
    h('whois <user>: Get information about <user>')
