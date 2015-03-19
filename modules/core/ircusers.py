# -*- coding: utf-8 -*-
from configs.module import Module
import irc.utils as utils


def init():
    m = Module('ircusers')
    m.set_help('Handle the User Lists.')
    m.add_base_hook('recv', recv)
    m.add_timer_hook(30 * 1000, timer)
    m.add_command_hook('whois',
        {
            'function': whois,
            'help': 'Get WHOIS information.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to view.'
                    }
                ],
            })
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
    if fp.sp.iscode('names'):
        channel = fp.Channel(fp, fp.sp.getsplit(4))
        names = fp.sp.text.split(' ')
        for i in range(len(names)):
            names[i] = utils.stripuser(names[i])
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
        if fp.sp.object not in fp.server.whoislist:
            fp.server.whoislist[fp.sp.object] = {}
        fp.server.whoislist[fp.sp.object]['ident'] = fp.sp.getsplit(4)
        fp.server.whoislist[fp.sp.object]['host'] = fp.sp.getsplit(5)
        fp.server.whoislist[fp.sp.object]['name'] = fp.sp.text
    elif fp.sp.iscode('330'):
        fp.server.whoislist[fp.sp.object]['authed'] = fp.sp.getsplit(4)
    elif fp.sp.iscode('318'):
        if fp.sp.object in fp.server.whoisbuffer:
            fp.server.whoislist[fp.sp.object]['done'] = True
            del fp.server.whoisbuffer[fp.server.whoisbuffer.index(fp.sp.object)]
    pass


def whois(fp, args):
    user = args.getlinstr('user')
    if user in fp.server.whoislist and 'done' in fp.server.whoislist[user]:
        t = fp.server.whoislist[user]
        return('%s!%s "%s" Authed: %s%s' % (
            user,
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
        return(str(channel.entry['names']))
    else:
        return(
            "That channel either doesn't exist or has no NAMES list yet.")


def timer():
    import running
    for server in running.working_servers:
        for channel in server.channels:
            if 'names' in channel:
                for name in channel['names']:
                    server.whois(name)
            server.write_cmd('NAMES', channel['channel'])
