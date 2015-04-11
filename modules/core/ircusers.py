# -*- coding: utf-8 -*-
from configs.module import Module
import irc.utils
import utils
import datetime
import traceback
import os
import db.text
import configs.locs


def init(options):
    server = options['server']
    path = configs.locs.userdb + '/lastseen.%s.py' % server.entry['settings']
    server.state['lastseen'] = db.text.DB(path)
    if os.path.exists(path):
        server.state['lastseen'].load()
    server.state['lastseen'].save()
    m = Module('ircusers')
    m.set_help('Handle the User Lists.')
    m.add_base_hook('recv', recv)
    m.add_timer_hook(90 * 1000, timer)
    m.add_command_hook('authme',
        {
            'function': authme,
            'help': 'Force a WHOIS on yourself.',
            'args': [],
            })
    m.add_command_hook('whois',
        {
            'function': whois,
            'help': 'Get WHOIS information.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to view.'
                    },
                {
                    'name': 'info',
                    'optional': True,
                    'help': 'Possible values: host'
                    },
                ],
            })
    m.add_command_hook('lastactive',
        {
            'function': lastseen,
            'help': 'Find when the nick was last active.',
            'args': [
                {
                    'name': 'chat',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Chat messages have priority.'
                    },
                {
                    'name': 'nick',
                    'optional': False,
                    'help': 'The nick to view.'
                    }
                ],
            })
    m.add_command_alias('lastseen', 'lastactive')
    m.add_command_hook('names',
        {
            'function': names,
            'help': 'Get NAMES information.',
            'args': [
                {
                    'name': 'channel',
                    'optional': False,
                    'help': 'The channel to view.'
                    }
                ],
            })
    return m


def recv(fp):
    try:
        if fp.sp.iscode('names'):
            channel = fp.Channel(fp, fp.sp.getsplit(4))
            names = fp.sp.text.split(' ')
            for i in range(len(names)):
                names[i] = irc.utils.stripuser(names[i])
            if 'newnames' not in channel.entry:
                channel.entry['newnames'] = []
            channel.entry['newnames'] += names
            for n in names:
                fp.server.whois(n)
        elif fp.sp.iscode('366'):
            channel = fp.Channel(fp, fp.sp.object)
            try:
                channel.entry['names'] = channel.entry['newnames']
                channel.entry['newnames'] = []
            except KeyError:
                pass
        elif fp.sp.iscode('311'):
            fp.server.whoislist[fp.sp.object] = {
                'op': [],
                'voice': [],
                'away': False,
                }
            fp.server.whoislist[fp.sp.object]['ident'] = fp.sp.getsplit(4)
            fp.server.whoislist[fp.sp.object]['host'] = fp.sp.getsplit(5)
            fp.server.whoislist[fp.sp.object]['name'] = fp.sp.text
        elif fp.sp.iscode('319'):
            o = []
            v = []
            for c in fp.sp.text.split():
                if c[0] == '@':
                    o.append(c[1:])
                elif c[0] == '+':
                    v.append(c[1:])
            fp.server.whoislist[fp.sp.object]['op'] = o
            fp.server.whoislist[fp.sp.object]['voice'] = v
        elif fp.sp.iscode('330'):
            fp.server.whoislist[fp.sp.object]['authed'] = fp.sp.getsplit(4)
        elif fp.sp.iscode('301'):
            fp.server.whoislist[fp.sp.object]['away'] = True
        elif fp.sp.iscode('318'):
            fp.server.whoislist[fp.sp.object]['done'] = True
        elif fp.sp.iscode('join'):
            fp.server.whois(fp.sp.sendernick)
            fp.server.do_base_hook('join', fp)
        elif fp.sp.iscode('part'):
            fp.server.do_base_hook('part', fp)
        elif fp.sp.iscode('quit'):
            channels = []
            for channel in fp.server.channels:
                if 'names' in channel:
                    if fp.sp.sendernick in channel['names']:
                        channels.append(channel['channel'])
            fp.server.do_base_hook('quit', fp, channels)
            fp.server.whois(fp.sp.sendernick)
        elif fp.sp.iscode('nick'):
            channels = []
            for channel in fp.server.channels:
                if 'names' in channel:
                    if fp.sp.sendernick in channel['names']:
                        channels.append(channel['channel'])
            fp.server.do_base_hook('nick', fp, channels)
            fp.server.whois(fp.sp.text)
    except KeyError:
        print((traceback.format_exc()))

    if fp.sp.sendernick:
        if fp.sp.sendernick not in fp.server.state['lastseen'].db():
            fp.server.state['lastseen'].db()[fp.sp.sendernick] = {
                }
        fp.server.state['lastseen'].db()[
            fp.sp.sendernick]['time'] = utils.utcepoch()
        fp.server.state['lastseen'].db()[fp.sp.sendernick][
            'action'] = "doing something unknown."
        if fp.sp.iscode('chat'):
            if fp.isquery():
                fp.server.state['lastseen'].db()[fp.sp.sendernick][
                    'action'] = "talking privately to me."
            elif fp.channel:
                t = "saying \"%s\" on %s." % (fp.sp.text,
                    fp.channel.entry['channel'])
                fp.server.state['lastseen'].db()[fp.sp.sendernick][
                'action'] = t
                fp.server.state['lastseen'].db()[fp.sp.sendernick][
                'maction'] = t
                fp.server.state['lastseen'].db()[fp.sp.sendernick][
                    'mtime'] = utils.utcepoch()
        else:
            fp.server.state['lastseen'].db()[fp.sp.sendernick][
            'action'] = "using %s %s." % (fp.sp.command.upper(),
                fp.sp.target if fp.sp.target else fp.sp.text)
        fp.server.state['lastseen'].save()


def authme(fp, args):
    fp.server.whoisbuffer = [fp.sp.sendernick] + fp.server.whoisbuffer
    return 'Attempt processed, check your access with: getrights'


def whois(fp, args):
    user = args.getlinstr('user')
    found = False
    for channel in fp.server.channels:
        if 'names' in channel:
            if user in channel['names']:
                found = True
    if not found:
        return '%s is not online.' % user
    if user in fp.server.whoislist and 'done' in fp.server.whoislist[user]:
        t = fp.server.whoislist[user]
        if 'info' in args.lin:
            if args.lin['info'] == 'host':
                return t['host']
            else:
                return 'That information cannot be provided.'
        return('%s%s, Host: %s, Name: "%s", Authed: %s%s' % (
            user,
            ' [Away]' if 'away' in t and t['away'] else '',
            t['host'],
            t['name'],
            'Yes' if 'authed' in t else 'No',
            ', as ' + t['authed'] if 'authed' in t and t['authed'] else '',
            ))
    else:
        return('No WHOIS information about %s.' % user)


def names(fp, args):
    channel = fp.Channel(fp, args.getlinstr('channel'))
    if channel.entry:
        return(utils.ltos(channel.entry['names']))
    else:
        return(
            "That channel either doesn't exist or has no NAMES list yet.")


def lastseen(fp, args):
    search = args.getlinstr('nick')
    if search not in fp.server.state['lastseen'].db():
        return 'I have never seen %s.' % search
    ts = fp.server.state['lastseen'].db()[search]['time']
    if 'mtime' in fp.server.state[
        'lastseen'].db()[search] and 'chat' in args.lin:
            ts = fp.server.state['lastseen'].db()[search]['mtime']
            return "%s was last seen chatting at %s UTC, %s" % (
                search,
                datetime.datetime.fromtimestamp(ts).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                fp.server.state['lastseen'].db()[search]['maction']
                )
    return "%s was last seen at %s UTC, %s" % (
        search,
        datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
        fp.server.state['lastseen'].db()[search]['action']
        )


def timer():
    import running
    for server in running.working_servers:
        for channel in server.channels:
            if 'names' in channel:
                for name in channel['names']:
                    server.whois(name)
            server.write_cmd('NAMES', channel['channel'])
