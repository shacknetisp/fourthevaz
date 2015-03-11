# -*- coding: utf-8 -*-
from configs.module import Module
import running


def init():
    m = Module('modop')
    m.set_help('Operate on modules.')
    m.add_command_hook('add',
        {
            'function': add,
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
    rlist = ['tests']
    flist = []
    for server in running.working_servers:
        for i in rlist:
            if server.delete_module(i):
                flist.append(i)
        server.load_commands()
    fp.reply('Removed: %s.' % flist)


def add(fp, args):
    rlist = ['tests']
    for server in running.working_servers:
        for i in rlist:
            server.add_module(i)
        server.load_commands()
    fp.reply('Added: %s.' % rlist)

