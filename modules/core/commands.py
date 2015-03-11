# -*- coding: utf-8 -*-
from configs.module import Module
import shlex


def init():
    m = Module('commands')
    m.set_help('Call the command system.')
    m.add_base_hook('recv', recv)
    return m


class Args:

    class ArgNotFoundError(Exception):

        def __init__(self, arg):
            self.arg = arg

        def __str(self):
            return 'Argument %s was not found.' % self.arg

    class ArgConflict(Exception):

        def __init__(self, arg, message):
            self.arg = arg
            self.message = message

        def __str(self):
            if self.arg is None:
                return '%s.' % (self.message)
            return '%s: %s.' % (self.arg, self.message)

    def __init__(self, t):
        self.text = t
        self.splittext = shlex.split(t)
        self.ssplittext = t.split()
        self.lin = {}

    def getidxstr(self, n):
        return self.splittext[n]

    def getlinstr(self, n, d=None):
        if n not in self.lin and d is not None:
            return d
        if n not in self.lin:
            raise Args.ArgNotFoundError(n)
        return self.lin[n]


def recv(fp):
    def mcdisabled(m):
        if fp.channel:
            if m in fp.channel.entry['disable']:
                return True
        return False
    if fp.sp.iscode('chat'):
        text = fp.sp.text
        prefix = fp.server.entry['prefix']
        if fp.channel:
            prefix = fp.channel.entry['prefix']
        elif fp.isquery():
            if text[0] != prefix:
                text = prefix + text
        args = None
        command = None
        modcall = False
        usedtext = ""
        wmodule = text[1:].split(' ')[0].split('.')[0].split(' ')[0]
        try:
            wcommand = text[1:].split(' ')[0].split('.')[1].split(' ')[0]
        except IndexError:
            wcommand = ""
        for m in fp.server.modules:
            if mcdisabled(m.name):
                fp.reply("This module is disabled here.")
                continue
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
                        fp.reply("You must specify a command.")
                        return
                    else:
                        fp.reply("%s is not in %s." % (wcommand, m.name))
                        return
                except IndexError:
                    fp.reply("This module is invalid.")
                    return
                break
        if not modcall:
            wcommand = wmodule
            for k in list(fp.server.commands.keys()):
                v = fp.server.commands[k]
                if wcommand == k:
                    if len(v) == 1:
                        if mcdisabled(v[list(v.keys())[0]]['module'].name):
                            fp.reply("This module is disabled here.")
                            return
                        command = v[list(v.keys())[0]]
                        usedtext = wcommand
                        break
                    else:
                        fp.reply('%s is provided by: %s, use <module>.%s.' % (
                            k, list(v.keys()), k))
                        return
        if command:
            t = ""
            try:
                t = text[len(usedtext) + 1:].strip()
            except IndexError:
                pass
            args = Args(t)
            counter = 0
            hasend = False
            hasoptional = False
            for a in command['args']:
                if 'end' in a and a['end']:
                    hasend = True
                elif a['optional'] and 'keyvalue' not in a:
                    hasoptional = True
            if hasend and hasoptional:
                raise Args.ArgConflict(None,
                    'Seperate optional and ending ' +
                    'linear arguments are not allowed.')
            #Standard Linear Args
            for a in command['args']:
                if len(args.splittext) > counter:
                    if ('end' not in a or not a['end']) and 'keyvalue' not in a:
                        args.lin[a['name']] = args.splittext[counter]
                counter += 1
            #Keyvalue Args
            for a in command['args']:
                if 'end' in a and 'keyvalue' in a and a['end']:
                    raise Args.ArgConflict(a['name'],
                        'Cannot be both ending and a keyvalue.')
                if 'keyvalue' in a:
                    for vi in range(len(args.splittext)):
                        if vi < counter:
                            v = args.splittext[vi]
                            if v.find('-' + a['name']) == 0:
                                try:
                                    args.lin[a['name']] = v[1:].split('=')[1]
                                except IndexError:
                                    pass
            #Ending Args
            counter = 0
            for a in command['args']:
                if len(args.splittext) > counter:
                    if 'end' in a and a['end']:
                        args.lin[a['name']] = ''
                        for i in range(counter, len(args.splittext)):
                            args.lin[a['name']] += ' ' + args.splittext[i]
                        args.lin[a['name']] = args.lin[a['name']].strip()
                        break
                counter += 1
            try:
                return command['function'](fp, args)
            except Args.ArgNotFoundError as e:
                fp.reply('Missing "%s", Usage: %s %s' % (e.arg, usedtext,
                Module.command_usage(command)))
        elif text[0] == prefix or fp.isquery():
            fp.reply("?")


