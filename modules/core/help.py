# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('help')
    m.set_help('Display help.')
    m.add_command_hook('help',
        {
            'function': showhelp,
            'help': 'Display help for a command.',
            'args': [
                {
                    'name': 'command',
                    'optional': False,
                    'help': 'Command to use.',
                    },
                {
                    'name': 'option',
                    'optional': True,
                    'help': 'Option to use.',
                    },
                ],
            })
    m.add_command_hook('modhelp',
        {
            'function': modhelp,
            'help': 'Display help for a module.',
            'args': [
                {
                    'name': 'module',
                    'optional': False,
                    'help': 'Module to use.',
                    },
                ],
            })
    return m


def showhelp(fp, args):
    wmodule = args.getlinstr(
        'command').split(' ')[0].split('.')[0].split(' ')[0]
    try:
        wcommand = args.getlinstr(
            'command').split(' ')[0].split('.')[1].split(' ')[0]
    except IndexError:
        wcommand = ""
    woption = args.getlinstr('option', '')
    #Logic
    command = None
    modcall = False
    for m in fp.server.modules:
        if wmodule == m.name:
            modcall = True
            usedtext = wmodule
            try:
                if len(m.command_hooks) == 1 and not wcommand:
                    command = m.command_hooks[
                        list(m.command_hooks.keys())[0]]
                elif wcommand in m.command_hooks:
                    command = m.command_hooks[wcommand]
                    usedtext += '.' + wcommand
                elif not wcommand:
                    return("You must specify a command.")
                else:
                    return("%s isn't in %s." % (wcommand, m.name))
            except IndexError:
                return("This module is invalid.")
            break
    if not modcall:
        wcommand = wmodule
        for k in list(fp.server.commands.keys()):
            v = fp.server.commands[k]
            if wcommand == k:
                if len(v) == 1:
                    command = v[list(v.keys())[0]]
                    usedtext = wcommand
                    break
                else:
                    return(
                        '%s is provided by: %s, use help <module>.%s.' % (
                        k, list(v.keys()), k))
    if not command:
        return('That command does not exist.')
    if woption:
        for c in command['args']:
            if c['name'] == woption:
                return('%s: %s' % (Module.command_single_usage(c), c['help']))
        return('Cannot find option %s in %s.%s.' % (
            woption, command['module'].name, command['name']))
    return(('%s.%s: %s -- %s %s' % (
        command['module'].name,
        command['name'],
        command['help'],
        command['name'],
        Module.command_usage(command))))


def modhelp(fp, args):
    for m in fp.server.modules:
        if m.name == args.getlinstr('module'):
            return('%s' % m.helptext)
    return('Unable to find module.')

