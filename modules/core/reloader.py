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
            'level': 50,
            'help': 'Reload all possible modules.',
            'args': [],
        })
    m.add_command_hook('reload',
        {
            'function': reload_list,
            'level': 50,
            'help': 'Reload a comma seperated list of modules.',
            'args': [
                {
                    'name': 'modules',
                    'optional': False,
                    'help': 'Modules to reload.'
                    },
                ],
        })
    return m


def reloadall(fp, args):
    moduleregistry.reloadscheduled = False
    moduleregistry.reload_all()
    for server in running.working_servers:
        server.reinit()
    return(('Reloaded all registered modules.'))


def reload_list(fp, args):
    rlist = args.getlinstr('modules').split(',')
    badlist = []
    goodlist = []
    for server in running.working_servers:
        for i in rlist:
            try:
                server.add_module(i)
                goodlist.append(i)
            except ImportError:
                badlist.append(i)
        server.load_commands()
    bt = ', could not reload: %s' % badlist
    if not badlist:
        bt = ''
    return('Reloaded: %s%s.' % (goodlist, bt))

