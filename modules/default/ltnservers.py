# -*- coding: utf-8 -*-
import configs.module
import configs.mload
import utils
from .redflare import redflare
from . import geoip


def init(options):
    server = options['server']
    if 'ltnservers' not in server.db or type(server.db[
        'ltnservers']) is not dict:
        server.db['ltnservers'] = {}
    m = configs.module.Module(__name__)
    m.set_help('Parse commands from servers.')
    m.add_command_hook('addserver', {
        'function': addserver,
        'help': 'Add a nick to the servers list.',
        'args': [
            {
                'name': 'nick',
                'optional': False,
                'help': 'Nick to add to the list'
                },
            {
                'name': 'address',
                'optional': False,
                'help': 'IP:port, use % for the IP to autodetect.'
                }
            ]
        })
    m.add_command_hook('removeserver', {
        'function': removeserver,
        'help': 'Removes a nick from the servers list.',
        'args': [
            {
                'name': 'nick',
                'optional': False,
                'help': 'Nick to remove from the list.'
                }
            ]
        })
    m.add_command_hook('listservers', {
        'function': listservers,
        'help': 'Show server list.',
        'args': []
        })
    m.add_base_hook('recv', recv)
    return m


def isredeclipse(fp):
    user = fp.sp.sendernick
    if user in fp.server.whoislist and 'done' in fp.server.whoislist[user]:
        return (fp.server.whoislist[user]['ident'] == '~redeclips')


def addserver(fp, args):
    if not ':'.join(args.getlinstr('address').split(':')[0:-1]):
        return 'Invalid Address'
    try:
        int(args.getlinstr('address').split(':')[-1])
    except ValueError:
        return 'Invalid Port'
    fp.server.db['ltnservers'][args.getlinstr('nick')] = args.getlinstr(
        'address')
    return '%s is now in the server list.' % args.getlinstr('nick')


def removeserver(fp, args):
    try:
        del fp.server.db['ltnservers'][args.getlinstr('nick')]
        return '%s has been removed from the server list.' % args.getlinstr(
            'nick')
    except KeyError:
        pass
    return '%s is not in the server list.' % args.getlinstr('nick')


def listservers(fp, args):
    results = []
    for k in fp.server.db['ltnservers']:
        results.append('%s:%s' % (k, fp.server.db['ltnservers'][k]))
    return 'Servers: ' + utils.ltos(results)


def recv(fp):
    commands = configs.mload.import_module_py(
        'commands', fp.server.entry['moduleset'], False)
    if fp.ltnserver():
        if fp.sp.iscode('QUIT') or fp.sp.iscode('PART'):
            for k in fp.server.state:
                if k.find('%s.authname.' % fp.sp.sendernick) == 0:
                    fp.server.state[k] = ''
        ptext = ""
        fp.sp.text = fp.sp.text.replace('\x0f', '')
        try:
            fp.user = utils.find_between(fp.sp.text, '<', '> ')
        except IndexError:
            fp.user = ''
        fp.setaccess("%s==" % fp.user)
        if isredeclipse(fp):
            authname = ""
            rf = redflare.RedFlare('http://redflare.ofthings.net/reports')
            entry = fp.server.db['ltnservers'][fp.sp.sendernick].split(':')
            host = ':'.join(entry[0:-1])
            if host == '%':
                host = fp.sp.host.split('@')[1]
            host = geoip.geoip(host)['query']
            if not host:
                host = ''
            for server in rf.servers:
                if server['host'] == host and server['port'] == int(entry[-1]):
                    for player in server['playerauths']:
                        if player[0] == fp.user:
                            authname = player[1]
            fp.setaccess("%s==:%s" % (fp.user, authname))
        try:
            text = fp.sp.text[fp.sp.text.index('> ') + 2:]
        except ValueError:
            return
        prefixt = fp.channel.entry['prefix'].split()
        possible = [
            fp.server.nick + ', ',
            fp.server.nick + ': ',
            ] + prefixt
        found = False
        prefix = prefixt[0]
        for p in possible:
            if text.find(p) == 0:
                found = True
                prefix = p
                break
        if not found:
            return
        ptext = text[len(prefix):]
        if ptext:
            fp.reply(commands.doptext(fp, ptext))