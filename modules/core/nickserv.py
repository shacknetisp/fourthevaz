# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('nickserv')
    m.set_help('Authenticate with NickServ.')
    m.add_base_hook('recv', recv)
    m.add_base_hook('joined', joined)
    m.add_command_hook('nickserv',
        {
            'level': 85,
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
    return m


def joined(server):
    if 'nspassword' in server.entry:
        server.write_cmd(
            'PRIVMSG', 'nickserv :identify %s' % server.entry['nspassword'])


def nickserv(fp, args):
    if fp.ltnserver():
        return "Must be called from IRC."
    fp.server.state['nsuser'] = fp.user
    action = args.getlinstr('action')
    if 'nspassword' not in fp.server.entry:
        return 'This server does not have an nspassword entry.'
    action = action.replace('%pass%', fp.server.entry['nspassword'])
    fp.server.write_cmd('PRIVMSG', 'nickserv :' + action)


def recv(fp):
    if fp.sp.sendernick.lower() == 'nickserv':
        if 'nsuser' in fp.server.state:
            fp.server.write_cmd('NOTICE', '%s :NickServ says: %s' % (
                fp.server.state['nsuser'], fp.sp.text))

