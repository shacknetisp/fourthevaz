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

    def __init__(self):
        self.lin = {}

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
        if 0 > fp.serverlevel or 0 > fp.channellevel:
            return
        if 'level' in command:
            if command['level'] > fp.accesslevel():
                fp.reply('You are level %d, but must be at least %d.' % (
                    fp.accesslevel(),
                    command['level']
                    ))
                return
        noquote = command['noquote'] if 'noquote' in command else False
        tt = ""
        try:
            tt = ptext[len(usedtext):].strip()
        except IndexError:
            pass
        t = ""
        lastch = ''
        elastch = ''
        quotes = []
        equotes = []
        inexec = False
        execlevel = 0
        inkv = False
        useargs = []
        args = Args()

        def doinkv(isend, t):
            if isend:
                t += ch
            var = t.split('=')[0]
            try:
                val = t.split('=')[1]
            except IndexError:
                val = ""
            if var in possibleargs:
                return 'You specified %s with a -' % var
            args.lin[var] = val
        for arg in command['args']:
            if 'end' in arg and arg['end']:
                continue
            if 'keyvalue' in arg:
                continue
            useargs.append(arg['name'])
        possibleargs = []
        for arg in command['args']:
            if 'keyvalue' in arg:
                continue
            possibleargs.append(arg['name'])
        execbuffer = ''
        for chi in range(len(tt)):
            ch = tt[chi]
            isbegin = (chi == 0)
            isend = (chi == len(tt) - 1)
            if inexec:
                if elastch == '\\':
                    execbuffer += ch
                else:
                    if ch in ['"', "'"] and not noquote:
                        if equotes:
                            if ch == equotes[-1]:
                                execbuffer += ch
                                equotes.pop(-1)
                                continue
                            else:
                                execbuffer += ch
                                continue
                        execbuffer += ch
                        equotes.append(ch)
                        continue
                    if ch == '<' and not equotes:
                        execlevel += 1
                        continue
                    elif ch == '>' and not equotes:
                        execlevel -= 1
                        if execlevel == 0:
                            inexec = False
                            r = doptext(fp, execbuffer)
                            if r is None:
                                return ("The command '%s' did not return." % (
                                    execbuffer)
                                + " Use quotes if you didn't want to run that.")
                            t += r
                            execbuffer = ''
                            if useargs and t:
                                args.lin[useargs[0]] = t
                                useargs.pop(0)
                                t = ''
                            continue
                    execbuffer += ch
                elastch = ch
            else:
                if lastch != '\\':
                    if ch == '\\':
                        lastch = ch
                        continue
                    if ch in ['"', "'"] and not noquote:
                        if quotes:
                            if ch == quotes[-1]:
                                quotes.pop(-1)
                                if inkv and isend:
                                    doinkv(False, t)
                                    t = ''
                                    inkv = False
                                    lastch = ' '
                                if useargs and isend:
                                    if t:
                                        args.lin[useargs[0]] = t
                                        useargs.pop(0)
                                        t = ''
                                        lastch = ' '
                                continue
                            else:
                                t += ch
                                continue
                        quotes.append(ch)
                        continue
                    if ch == ' ' or isend:
                        if not quotes:
                            if inkv:
                                doinkv(isend, t)
                                t = ''
                                inkv = False
                                lastch = ' '
                                continue
                            if useargs:
                                if isend:
                                    t += ch
                                if t:
                                    args.lin[useargs[0]] = t
                                    useargs.pop(0)
                                    t = ''
                                    lastch = ' '
                                continue
                    if ch == '-' and command['haskeyvalue']:
                        try:
                            if tt[chi + 1].isalpha():
                                if isbegin or lastch == ' ':
                                    if not quotes and not inkv:
                                        inkv = True
                                        if useargs and t:
                                            args.lin[useargs[0]] = t
                                            useargs.pop(0)
                                        t = ''
                                        continue
                        except IndexError:
                            pass
                    if ((noquote and ch == '*' and lastch == '<') or
                    (not noquote and ch == '<')):
                        if not quotes:
                            if (noquote and ch == '*' and lastch == '<'):
                                t = t[0:-1]
                            inexec = True
                            execlevel += 1
                            continue
                    t += ch
                else:
                    t += ch
                lastch = ch
        if quotes:
            return 'You are missing an ending quotation mark!'
        if inexec:
            return 'You are missing an ending ">"!'
        if t:
            for arg in command['args']:
                if 'end' in arg and arg['end']:
                    args.lin[arg['name']] = t
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
                    try:
                        acint = int(ac)
                    except ValueError:
                        acint = 0
                    if c == '$' and ac == "#":
                        if hadall:
                            return "Arguments after $* are not supported."
                        found = True
                        try:
                            result = shlex.split(args)[lastusedindex]
                            lastusedindex += 1
                        except IndexError:
                            return "Too few arguments!"
                        except ValueError:
                            return "Missing ending quote!"
                        t = t[0:ic] + (
                            result + t[ic + 2:])
                        break
                    if c == '$' and ac == "*":
                        found = True
                        try:
                            result = ' '.join(shlex.split(args)[
                                lastusedindex:])
                        except IndexError:
                            pass
                        except ValueError:
                            return "Missing ending quote!"
                        hadall = True
                        t = t[0:ic] + (
                            result + t[ic + 2:])
                        break
                    if c == '$' and acint:
                        found = True
                        try:
                            result = shlex.split(args)[acint - 1]
                        except IndexError:
                            return "Too few arguments!"
                        except ValueError:
                            return "Missing ending quote!"
                        t = t[0:ic] + (
                            result + t[ic + 2:])
                        break
        return doptext(fp, t, count)
    else:
        if fp.isquery():
            return("?")
        if len(ptext.split(' ')[0].split('.')) == 1:
            for m in fp.server.modules:
                if ptext.split(' ')[0].split('.')[0] == m.name:
                    return doptext(fp,
                        'echo <*modhelp %s> <*qecho "--"> <*list %s>' % (
                        m.name, m.name))
    return None


def recv(fp):
    if fp.sp.iscode('chat'):
        try:
            if fp.sp.text[0] == '\x01':
                st = fp.sp.text.strip('\x01')
                try:
                    fp.ctcptext = " ".join(st.split()[1:])
                except IndexError:
                    fp.ctcptext = ""
                fp.server.do_base_hook('ctcp.%s' % st.split()[0].lower(), fp)
                return
        except Exception as e:
            r = 'Uncaught ' + str(type(e).__name__) + '!'
            fp.reply(r)
            print((traceback.format_exc()))
            return
        if fp.sp.sendernick in ['ChanServ', 'NickServ']:
            return
        if fp.ltnserver():
            return
        text = fp.sp.text
        prefixt = fp.server.entry['prefix'].split()
        if fp.channel:
            prefixt = fp.channel.entry['prefix'].split()
        elif fp.isquery():
            for prefix in prefixt:
                if text.find(prefix) != 0:
                    text = prefix + text
                    break
        possible = [
            fp.server.nick + ', ',
            fp.server.nick + ': ',
            ] + prefixt
        found = False
        prefix = prefixt[0]
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


