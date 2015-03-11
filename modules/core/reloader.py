# -*- coding: utf-8 -*-
from configs.module import Module
import moduleregistry
import running


def init():
    m = Module('reloader')
    m.set_help('Reload various parts of the bot.')
    m.add_command_hook('reloadall',
        {
            'function': reloadall,
            'help': 'Reload all possible modules.',
            'args': [],
        })
    m.add_command_hook('reload',
        {
            'function': reload_list,
            'help': 'Reload some modules.',
            'args': [],
        })
    return m


def reloadall(fp, args):
    moduleregistry.reloadscheduled = False
    moduleregistry.reload_all()
    for server in running.working_servers:
        server.reinit()
    fp.reply('Reloading all registered modules.')


def reload_list(fp, args):
    rlist = ['tests', 'reloader']
    for server in running.working_servers:
        for i in rlist:
            server.add_module(i)
    fp.reply('Reloading: %s.' % rlist)

