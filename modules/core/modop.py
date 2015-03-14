# -*- coding: utf-8 -*-
from configs.module import Module
import running


def init():
    m = Module('modop')
    m.set_help('Operate on modules.')
    m.add_command_hook('add',
        {
            'function': add,
            'level': 50,
            'help': 'Add modules.',
            'args': [
                {
                    'name': 'modules',
                    'optional': False,
                    'help': 'The modules to operate on.'
                    },
                ],
        })
    m.add_command_hook('remove',
        {
            'function': remove,
            'level': 50,
            'help': 'Remove modules.',
            'args': [
                {
                    'name': 'modules',
                    'optional': False,
                    'help': 'The modules to operate on.'
                    },
                ],
        })
    return m


def remove(fp, args):
    rlist = args.getlinstr('modules').split(',')
    goodlist = []
    badlist = []
    for server in running.working_servers:
        for i in rlist:
            if server.delete_module(i):
                goodlist.append(i)
            else:
                badlist.append(i)
        server.load_commands()
    bt = ', could not remove: %s' % badlist
    if not badlist:
        bt = ''
    fp.reply('Removed: %s%s.' % (goodlist, bt))


def add(fp, args):
    rlist = args.getlinstr('modules').split(',')
    goodlist = []
    badlist = []
    for server in running.working_servers:
        for i in rlist:
            try:
                server.add_module(i)
                goodlist.append(i)
            except ImportError:
                badlist.append(i)
        server.load_commands()
    bt = ', could not add: %s' % badlist
    if not badlist:
        bt = ''
    fp.reply('Added: %s%s.' % (goodlist, bt))

