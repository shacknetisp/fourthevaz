# -*- coding: utf-8 -*-
from configs.module import Module
import shlex
import utils
import traceback


def init():
    m = Module('commands')
    m.set_help('Call the command system.')
    m.add_base_hook('recv', recv)
    return m


class NoEndToken(Exception):

        def __init__(self, arg):
            self.arg = arg
            self.msg = 'Missing parser token ending "%s".' % self.arg

        def __str(self):
            return self.msg


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

    def __init__(self, t, noshlex):
        self.text = t
        if noshlex:
            self.splittext = t.split(' ')
        else:
            self.splittext = shlex.split(t)
        self.lin = {}

    def getidxstr(self, n):
        return self.splittext[n]

    def getlinstr(self, n, d=None):
        if n not in self.lin and d is not None:
            return d
        if n not in self.lin:
            raise Args.ArgNotFoundError(n)
        return self.lin[n]


def doptext(fp, p_ptext, count=100):
    count -= 1
    if count < 0:
        raise RuntimeError('doptext recursion limit reached.')

    def mcdisabled(m):
        if fp.channel:
            if m in fp.channel.entry['disable']:
                return True
        return False
    args = None
    command = None
    modcall = False
    usedtext = ""
    ptext = p_ptext
    wmodule = ptext.split(' ')[0].split('.')[0].split(' ')[0]
    waswcommand = False
    try:
        wcommand = ptext.split(' ')[0].split('.')[1].split(' ')[0]
        waswcommand = True
    except IndexError:
        wcommand = ""
    for m in fp.server.modules:
        if not waswcommand:
            break
        if mcdisabled(m.name):
            fp.reply("This module is disabled here.")
            continue
        if wmodule == m.name:
            modcall = True
            usedtext = wmodule
            if not wcommand and wmodule in m.command_hooks:
                wcommand = wmodule
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
                        k, utils.ltos(list(v.keys())), k))
                    return
    if command:
        if 'level' in command:
            if command['level'] > fp.accesslevel():
                fp.reply('You are level %d, but must be at least %d.' % (
                    fp.accesslevel(),
                    command['level']
                    ))
                return
        t = ""
        try:
            t = ptext[len(usedtext):].strip()
        except IndexError:
            pass
        found = True
        while found:
            found = False
            for ic in range(len(t)):
                try:
                    bc = t[ic - 1]
                except IndexError:
                    bc = ''
                c = t[ic]
                try:
                    ac = t[ic + 1]
                except IndexError:
                    ac = ''
                if bc != '"':
                    if c == '<' and ac == "*":
                        found = True
                        endi = t.rfind('>')
                        if endi == -1:
                            raise NoEndToken('>')
                        result = doptext(fp, t[ic + 2:endi], count)
                        if not result:
                            fp.reply('That command does not return.')
                            return
                        t = t[0:ic] + (
                            result + t[endi + 1:])
                        break
        noshlex = command['noshlex'] if 'noshlex' in command else False
        args = Args(t, noshlex)
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
        if command['haskeyvalue']:
            for a in command['args']:
                if len(args.splittext) > counter:
                    if ('end' not in a or not a['end']) and 'keyvalue' not in a:
                        args.lin[a['name']] = args.splittext[counter]
                        counter += 1
            #Option Args
            lastval = ""
            argsdefv = ""
            ar = args.splittext[counter:]
            ok = True
            fstr = ""
            for i in ar:
                if i[0] == '-' and ok:
                    var = i.split("=")[0][1:]
                    try:
                        val = i.split("=")[1]
                        fstr += "-" + var + "=" + val + " "
                    except IndexError:
                        val = ""
                        fstr += "-" + var + " "
                    args.lin[var] = val
                    for arg in command['args']:
                        aliases = arg['aliases'] if 'aliases' in arg else []
                        if arg['name'] == var or var in aliases:
                            args.lin[arg['name']] = val
                            for al in aliases:
                                args.lin[al] = val
                    lastval = i
                else:
                    fstr += i + " "
                ok = False
            fstr = fstr.strip()
            argsv = fstr
            if lastval:
                argsdefv = argsv[
                argsv.rfind(lastval) + len(lastval):]
                argsdefv = argsdefv[argsdefv.find('" ') + 2:]
            else:
                argsdefv = argsv
            if len(argsdefv) > 0:
                if argsdefv[0] == '"' or argsdefv[0] == "'":
                    argsdefv = argsdefv[1:]
                if argsdefv[-1] == '"' or argsdefv[-1] == "'":
                    argsdefv = argsdefv[:-1]
            for a in command['args']:
                if 'end' in a and a['end']:
                    if argsdefv:
                        args.lin[a['name']] = argsdefv
                elif 'keyvalue' not in a:
                    if a['optional']:
                        raise Args.ArgConflict(None,
                        'All arguments must be ' +
                        'either keyvalue or not optional.')

        else:
            #Standard Linear Args
            for a in command['args']:
                if len(args.splittext) > counter:
                    if ('end' not in a or not a['end']):
                        args.lin[a['name']] = args.splittext[counter]
                counter += 1
        try:
            extra = {
                }
            if command['function'].__code__.co_argcount == 3:
                return command['function'](fp, args, extra)
            elif command['function'].__code__.co_argcount == 2:
                return command['function'](fp, args)
            else:
                raise TypeError('Hook for command %s.%s is invalid!' % (
                    command['module'].name,
                    command['name'],
                    ))
        except Args.ArgNotFoundError as e:
            fp.reply('Missing "%s", Usage: %s %s' % (e.arg, usedtext,
            Module.command_usage(command)))
    elif wcommand in fp.get_aliases():
        t = fp.get_aliases()[wcommand]
        try:
            args = ' '.join(p_ptext.split(' ')[1:])
        except IndexError:
            args = ""
        found = True
        lastusedindex = 0
        hadall = False
        while found:
            found = False
            for ic in range(len(t)):
                try:
                    bc = t[ic - 1]
                except IndexError:
                    bc = ''
                c = t[ic]
                try:
                    ac = t[ic + 1]
                except IndexError:
                    ac = ''
                if bc != '"':
                    if c == '$' and ac == "#":
                        if hadall:
                            return "Arguments after $* are not supported."
                        found = True
                        try:
                            result = shlex.split(args)[lastusedindex]
                            lastusedindex += 1
                        except IndexError:
                            return "Too few arguments!"
                        t = t[0:ic] + (
                            result + t[ic + 2:])
                        print(t)
                        break
                    if c == '$' and ac == "*":
                        found = True
                        try:
                            result = ' '.join(shlex.split(args)[
                                lastusedindex:])
                        except IndexError:
                            pass
                        hadall = True
                        t = t[0:ic] + (
                            result + t[ic + 2:])
                        break
        return doptext(fp, t, count)
    elif fp.isquery():
        fp.reply("?")
    return None


def recv(fp):
    if fp.sp.iscode('chat'):
        if fp.sp.sendernick in ['ChanServ', 'NickServ']:
            return
        text = fp.sp.text
        prefix = fp.server.entry['prefix']
        if fp.channel:
            prefix = fp.channel.entry['prefix']
        elif fp.isquery():
            if text.find(prefix) != 0:
                text = prefix + text
        possible = [
            prefix,
            fp.server.nick + ', ',
            fp.server.nick + ': ',
            ]
        found = False
        for p in possible:
            if text.find(p) == 0:
                found = True
                prefix = p
                break
        if not found:
            return
        ptext = text[len(prefix):]
        try:
            r = doptext(fp, ptext)
        except NoEndToken as e:
            r = e.msg
        except Exception as e:
            r = 'Uncaught ' + str(type(e).__name__) + '!'
            print((traceback.format_exc()))
        if r:
            fp.reply(r)


