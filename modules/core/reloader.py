# -*- coding: utf-8 -*-
from configs.module import Module
import moduleregistry
import running
import utils


def init():
    m = Module('reloader')
    m.set_help('Reload various parts of the bot.')
    m.add_timer_hook(2.5 * 1000, timer)
    m.add_command_hook('reloadall',
        {
            'function': reloadall,
            'rights': ['admin'],
            'help': 'Reload all possible modules.',
            'args': [],
        })
    m.add_command_hook('reload',
        {
            'function': reload_list,
            'rights': ['admin'],
            'help': 'Reload a comma seperated list of modules.',
            'args': [
                {
                    'name': 'modules',
                    'optional': False,
                    'help': 'Modules to reload.'
                    },
                ],
        })
    m.add_short_command_hook(reinit,
        'reinit::Reload all possible files.', [], 75)
    return m


def timer():
    if moduleregistry.reloadscheduled:
        moduleregistry.reloadscheduled = False
        moduleregistry.reload_all()
        for server in running.working_servers:
            server.reinit()


def reinit(fp, args):
    running.reinit = True
    return "Re-connecting to all servers."


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
                if i not in goodlist:
                    goodlist.append(i)
            except ImportError:
                if i not in badlist:
                    badlist.append(i)
        server.load_commands()
    bt = '; could not reload: %s' % utils.ltos(badlist)
    if not badlist:
        bt = ''
    return('Reloaded: %s%s.' % (utils.ltos(goodlist), bt))

