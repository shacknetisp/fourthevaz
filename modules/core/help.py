# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('help')
    m.set_help('Display help.')
    m.add_command_hook('help',
        {
            'function': showhelp,
            'help': 'Display help.',
            'args': [
                {
                    'name': 'module',
                    'optional': True,
                    'help': 'Module to use.',
                    },
                {
                    'name': 'command',
                    'optional': True,
                    'help': 'Command to use.',
                    },
                {
                    'name': 'option',
                    'optional': True,
                    'help': 'Option to use.',
                    },
                ],
            })
    return m


def showhelp(fp, args):
    t = {
        'command': 'help',
        'module': '',
        'option': '',
        }
    command = None
    modcall = False
    for m in fp.server.modules:
        if t['module'] == m.name:
            modcall = True
            if t['command'] in m.command_hooks:
                command = m.command_hooks[t['command']]
            else:
                fp.reply(('%s: %s' % (
                    m.name, m.helptext)))
                return
            break
    if not modcall:
        for k in list(fp.server.commands.keys()):
            v = fp.server.commands[k]
            if t['command'] == k:
                if len(v) == 1:
                    command = v[list(v.keys())[0]]
                    break
                else:
                    fp.reply('%s is provided by: %s, use: help <module> %s.' % (
                        k, list(v.keys()), k))
                    return
    optiontext = ""
    for i in command['args']:
        topt = '<' + i['name'] + '>'
        if i['optional']:
            topt = '[' + topt + ']'
        optiontext += topt + ' '
    fp.reply(('%s from %s: %s -- %s %s' % (
        t['command'],
        command['module'].name,
        command['help'],
        t['command'],
        optiontext.strip())))

