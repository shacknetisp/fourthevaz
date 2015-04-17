# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('nickserv')
    m.set_help('Authenticate with NickServ.')
    m.add_base_hook('recv', recv)
    m.add_base_hook('joined', joined)
    m.add_command_hook('nickserv',
        {
            'rights': ['admin'],
            'help': 'Interact with NickServ, replace %pass% with the password.',
            'function': nickserv,
            'args': [
                {
                    'name': 'action',
                    'optional': False,
                    'help': 'Command to send to NickServ.',
                    'end': True,
                    },
                ]
            })
    m.add_base_hook('commands.ignore', commands_ignore)
    return m


def commands_ignore(fp, ignore):
    if fp.sp.sendernick.lower() in [
        'nickserv',
        'chanserv',
        ]:
            ignore['ignore'] = True


def joined(server):
    if server.auth[0] == 'nickserv':
        server.write_cmd(
            'PRIVMSG', 'nickserv :identify %s %s' % (server.auth[1],
                server.auth[2]))


def nickserv(fp, args):
    if fp.external():
        return "Must be called from IRC."
    fp.server.state['nsuser'] = fp.user
    action = args.getlinstr('action')
    if fp.server.auth[0] == 'nickserv':
        return 'This server does not have a nickserv entry.'
    action = action.replace('%pass%', fp.server.auth[2])
    fp.server.write_cmd('PRIVMSG', 'nickserv :' + action)


def recv(fp):
    if fp.sp.sendernick.lower() == 'nickserv':
        if 'nsuser' in fp.server.state:
            fp.server.write_cmd('NOTICE', '%s :NickServ says: %s' % (
                fp.server.state['nsuser'], fp.sp.text))

