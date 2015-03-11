# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('commands')
    m.set_help('Call the command system.')
    m.add_base_hook('recv', recv)
    return m


class Args:
    def __init__(self):
        pass


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
        function = None
        modcall = False
        for m in fp.server.modules:
            if mcdisabled(m.name):
                if 'mcd_message' in fp.server.entry:
                    fp.reply(fp.server.entry['mcd_message'])
                continue
            if text.split()[0] == prefix + m.name:
                modcall = True
                try:
                    if len(m.command_hooks) == 1 and len(text.split()) <= 1:
                        function = m.command_hooks[
                            list(m.command_hooks.keys())[0]]['function']
                    elif text.split()[1] in m.command_hooks:
                        function = m.command_hooks[text.split()[1]]['function']
                    else:
                        if 'mnf_message' in fp.server.entry:
                            fp.reply(fp.server.entry['mnf_message'])
                except IndexError:
                    if 'mcne_message' in fp.server.entry:
                        fp.reply(fp.server.entry['mcne_message'])
                    return
                break
        if not modcall:
            for k in list(fp.server.commands.keys()):
                v = fp.server.commands[k]
                if text.split()[0] == prefix + k:
                    if len(v) == 1:
                        if mcdisabled(v[list(v.keys())[0]]['module'].name):
                            if 'mcd_message' in fp.server.entry:
                                fp.reply(fp.server.entry['mcd_message'])
                            return
                        function = v[list(v.keys())[0]]['function']
                        break
                    else:
                        fp.reply('%s is provided by: %s, use <module> %s.' % (
                            k, list(v.keys()), k))
                        return
        if function:
            function(fp, args)
        elif text[0] == prefix or fp.isquery():
            if 'cnf_message' in fp.server.entry:
                fp.reply(fp.server.entry['cnf_message'])


