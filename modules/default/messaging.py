# -*- coding: utf-8 -*-
from configs.module import Module
import utils
import configs.match
import irc.utils


def init(options):
    if 'messaging.tells' not in options['server'].db:
        options['server'].db['messaging.tells'] = []
    m = Module(__name__)
    m.set_help('Message system.')
    m.add_command_hook('tell',
        {
            'function': tell,
            'rights': ['normal'],
            'help': 'Give <nick> <message> when <nick> is online. (No shlex.)',
            'noquote': True,
            'args': [
                {
                    'name': 'nick',
                    'optional': False,
                    'help': 'Nick to send to, you can use wildcards.',
                    },
                {
                    'name': 'message',
                    'optional': False,
                    'help': 'Message to send.',
                    'end': True,
                    },
                ],
            })
    m.add_base_hook('recv', recv)
    return m


def tell(fp, args):
    nick = args.getlinstr('nick')
    oldnicks = nick.split(',')
    nicks = nick.split(',')
    message = '<<%s>> %s' % (fp.user, args.getlinstr('message'))
    for nick in nicks:
        fp.server.db['messaging.tells'].append((nick, message))
        for channel in fp.server.channels:
            if 'names' in channel:
                for n in channel['names']:
                    if configs.match.match(
                    n, nick, True):
                        fp.server.write_cmd('PRIVMSG', ('%s :' % n) +
                        irc.utils.ctcp('PING Hello!'))
    return 'Will send "%s" to "%s"' % (args.getlinstr('message'),
                        utils.ltos(oldnicks))


def recv(fp):
    if fp.sp.iscode('chat') or fp.sp.iscode('join'):
        server = fp.server
        name = fp.sp.sendernick
        tod = []
        for i in range(len(server.db['messaging.tells'])):
            n = server.db['messaging.tells'][i]
            if configs.match.match(
                name, n[0], True):
                    server.write_cmd(
                        'PRIVMSG', '%s :%s' % (name, n[1]))
                    tod.append(i)
        server.db[
            'messaging.tells'] = utils.remove_indices(
            server.db['messaging.tells'], tod)
