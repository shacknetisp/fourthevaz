# -*- coding: utf-8 -*-
import utils
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
    if 'command' not in args.lin:
        return ('Basic Commands: ' +
        '`list`, `modhelp <module>`, `help <command>`.')
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
    seealso = ""
    for m in fp.server.modules:
        if wmodule == m.name:
            modcall = True
            usedtext = wmodule
            if not wcommand and wmodule in m.command_hooks:
                wcommand = wmodule
                seealso = " (See also: modhelp %s)" % m.command_hooks[
                    wmodule]['name']
            try:
                if len(m.command_hooks) == 1 and not wcommand:
                    command = m.command_hooks[
                        list(m.command_hooks.keys())[0]]
                elif wcommand in m.command_hooks:
                    command = m.command_hooks[wcommand]
                    usedtext += '.' + wcommand
                elif not wcommand:
                    return(fp.execute('modhelp ' + m.name))
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
                        k, utils.ltos(list(v.keys())), k))
    if not command:
        if wcommand in fp.get_aliases():
            return '<%s>' % (fp.get_aliases()[wcommand])
        v = fp.server.import_module('commands.executer', False).execute(
            fp.server,
            wcommand,
            "",
            {'FOURTHEVAZ': 'help'},
            )
        if v is not None:
            return v
        return('That command does not exist.')
    if woption:
        for c in command['args']:
            if c['name'] == woption:
                return('%s: %s' % (Module.command_single_usage(c), c['help']))
        return('Cannot find option %s in %s.%s.' % (
            woption, command['module'].name, command['name']))
    return(('%s.%s (%s): %s -- %s %s %s' % (
        command['module'].name,
        command['name'],
        utils.ltos(command['rights'], ' '),
        command['help'],
        command['name'],
        Module.command_usage(command), seealso)))


def modhelp(fp, args):
    for m in fp.server.modules:
        if m.name == args.getlinstr('module'):
            return('%s -- %s' % (m.helptext, fp.execute('list ' + m.name)))
    return('Unable to find module %s.' % args.getlinstr('module'))

