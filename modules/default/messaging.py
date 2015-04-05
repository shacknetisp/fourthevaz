# -*- coding: utf-8 -*-
from configs.module import Module
import utils
import configs.match
import running


def init(options):
    if 'messaging.tells' not in options['server'].db:
        options['server'].db['messaging.tells'] = []
    m = Module(__name__)
    m.set_help('Message system.')
    m.add_command_hook('tell',
        {
            'function': tell,
            'level': 1,
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
    m.add_timer_hook(30 * 1000, timer)
    return m


def tell(fp, args):
    nick = args.getlinstr('nick')
    oldnicks = nick.split(',')
    nicks = nick.split(',')
    message = '<<%s>> %s' % (fp.user, args.getlinstr('message'))
    for nick in nicks:
        fp.server.db['messaging.tells'].append((nick, message))
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
                        'NOTICE', '%s :%s' % (name, n[1]))
                    tod.append(i)
        server.db[
            'messaging.tells'] = utils.remove_indices(
            server.db['messaging.tells'], tod)


def timer():
    for server in running.working_servers:
        for channel in server.channels:
            if 'names' in channel:
                for name in channel['names']:
                    tod = []
                    for i in range(len(server.db['messaging.tells'])):
                        n = server.db['messaging.tells'][i]
                        if configs.match.match(
                            name, n[0], True):
                                server.write_cmd(
                                    'NOTICE', '%s :%s' % (name, n[1]))
                                tod.append(i)
                    server.db[
                        'messaging.tells'] = utils.remove_indices(
                        server.db['messaging.tells'], tod)