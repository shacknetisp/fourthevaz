# -*- coding: utf-8 -*-
from configs.module import Module
import utils
import configs.match


def init(options):
    if 'messaging.tells' not in options['server'].db:
        options['server'].db['messaging.tells'] = []
    m = Module(__name__)
    m.set_help('Message system.')
    m.add_command_hook('tell',
        {
            'function': tell,
            'help': 'Give <nick> <message> when <nick> is online. (No shlex.)',
            'noshlex': True,
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
    m.add_base_hook('join', join)
    return m


def tell(fp, args):
    nick = args.getlinstr('nick')
    oldnicks = nick.split(',')
    nicks = nick.split(',')
    message = '<%s tells you> %s' % (fp.user, args.getlinstr('message'))
    for channel in fp.server.channels:
        if 'names' in channel:
            for name in channel['names']:
                tod = []
                for nicki in range(len(nicks)):
                    if configs.match.match(
                        name, nicks[nicki], True):
                            fp.server.write_cmd(
                                'NOTICE', '%s :%s' % (name, message))
                            tod.append(nicki)
                nicks = utils.remove_indices(nicks, tod)
    for nick in nicks:
        fp.server.db['messaging.tells'].append((nick, message))
    return 'Will send "%s" to "%s"' % (message, utils.ltos(oldnicks))


def join(fp):
    tod = []
    for i in range(len(fp.server.db['messaging.tells'])):
        n = fp.server.db['messaging.tells'][i]
        if configs.match.match(fp.sp.sendernick, n[0], True):
            fp.server.write_cmd('NOTICE', '%s :%s' % (fp.sp.sendernick, n[1]))
            tod.append(i)
    fp.server.db['messaging.tells'] = utils.remove_indices(
        fp.server.db['messaging.tells'], tod)