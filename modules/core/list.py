# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('list')
    m.set_help('Display command lists.')
    m.add_command_hook('list',
        {
            'function': clist,
            'help': 'Display a command/module list.',
            'args': [
                {
                    'name': 'modules',
                    'optional': True,
                    'help': 'Module(s) to list.',
                    },
                ],
            })
    m.add_command_hook('commands',
        {
            'function': commands,
            'help': 'Display all commands.',
            'args': [],
            })
    return m


def clist(fp, args):
    wmodules = args.getlinstr('modules', '').split(',')
    if not args.getlinstr('modules', ''):
        wmodules = []
    output = []
    if wmodules:
        for m in fp.server.modules:
            if m.name in wmodules or not wmodules:
                for a in m.command_hooks:
                    if a not in output:
                        output.append(a)
    else:
        for m in fp.server.modules:
            output.append(m.name)
    fp.reply('%s' % (
        output
        ))


def commands(fp, args):
    commands = []
    for m in fp.server.modules:
        for a in m.command_hooks:
            if a not in commands:
                commands.append(a)
    fp.reply('%s' % (
        commands
        ))


