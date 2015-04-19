# -*- coding: utf-8 -*-
ctcplist = []
"""List of CTCP hooks."""
alllist = []
"""List of all hooks."""
import utils
import string


class Module:

    def __init__(self, name):
        self.set = ""
        self.base_hooks = {}
        self.command_hooks = {}
        self.timer_hooks = []
        self.helptext = ""
        self.name = name.split('.')[-1]
        self.aliases = {}
        self.rights = []
        self.implicitrights = {}

    def add_implicit_rights(self, d):
        """
        Add implicit rights as follows:
        'ifhavethis': ['getthis', 'andthis']
        or
        '%,op': '%,normal'
        """
        for right in d:
            for implies in [d[right]] if type(d[right]) is str else d[right]:
                if right not in self.implicitrights:
                    self.implicitrights[right] = []
                if implies not in self.implicitrights[right]:
                    self.implicitrights[right].append(implies)

    def add_alias(self, name, content):
        """Add an alias <name> with <content>."""
        self.aliases[name] = content

    def add_aliases(self, aliases):
        """
        Add multiple aliases with format:
        'name': 'content'
        """
        self.aliases = utils.merge_dicts(self.aliases, aliases)

    def add_rights(self, rights):
        """Add a right to the list of rights that can be set."""
        self.rights += rights

    def set_help(self, helptext):
        """Set the module description."""
        self.helptext = helptext

    def add_base_hook(self, hook, f):
        """Call <f> upon base hook <hook>."""
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
        if hook not in alllist:
            alllist.append(hook)
        self.base_hooks[hook].append(f)
        try:
            if hook.split('.')[0] == 'ctcp':
                c = hook.split('.')[1].upper()
                if c not in ctcplist:
                    ctcplist.append(c)
        except IndexError:
            pass

    def get_base_hook(self, hook):
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
        return self.base_hooks[hook]

    def add_timer_hook(self, time, f):
        """Every <time> milliseconds, call <f>. (The timer is not exact.)"""
        self.timer_hooks.append({
            'time': time,
            'lasttime': 0,
            'function': f,
            })

    def add_command_hook(self, hook, p_d):
        """
        Add a long command hook to <hook> with data <p_d>.
        See examples/module.py for more information.
        """
        if hook[0] in string.punctuation:
            raise ValueError('Punctuation may not start a command hook.')
        d = p_d
        if 'rights' not in d:
            d['rights'] = []
        d['module'] = self
        d['name'] = hook
        d['haskeyvalue'] = False
        for i in d['args']:
            if 'keyvalue' in i:
                d['haskeyvalue'] = True
        self.command_hooks[hook] = d

    def add_short_command_hook(self, function, string, argstrs, rights=[],
        noquote=False):
        """
        Add a short command hook.
        <function>: Function to call.
        <string>: Command and help text in this format: 'command::Command help.'
        <argstrs>: List of args in this format:
            ['anarg...::Help here.', '[-kv2]::Another description.']
        <rights>: List of rights required. ('%,normal', 'admin', etc.)
        <noquote>: Interpret quote characters literally?
        """
        args = []
        for arg in argstrs:
            ad = {
                'optional': False,
                'help': arg.split('::')[1],
                'end': False,
                }
            arg = arg.split('::')[0]
            if arg[0] == '[':
                ad['optional'] = True
                arg = arg[1:-1]
            if arg[0] == '-':
                ad['keyvalue'] = arg.split('=')[1] if arg.count('=') else ''
                arg = arg[1:].split('=')[0]
            else:
                try:
                    if arg[-3:] == '...':
                        ad['end'] = True
                        arg = arg[:-3]
                except IndexError:
                    pass
            ad['name'] = arg
            args.append(ad)
        self.add_command_hook(string.split('::')[0], {
            'function': function,
            'help': string.split('::')[1],
            'noquote': noquote,
            'args': args,
            'rights': rights,
            })

    def add_command_alias(self, alias, hook):
        """Make the command <alias> point to the command <hook>."""
        self.command_hooks[alias] = self.command_hooks[hook]

    def command_single_usage(i):
        base = i['name']
        if 'aliases' in i and i['aliases']:
            base = "{"
            base += i['name'] + ','
            base += ','.join(i['aliases'])
            base += "}"
        if 'end' in i and i['end']:
            base = base + '...'
        topt = '<' + base + '>'
        if 'keyvalue' in i:
            if i['keyvalue']:
                topt = '-' + base + '=<' + i['keyvalue'] + '>'
            else:
                topt = '-' + base
        else:
            topt = '<' + base + '>'
        if i['optional']:
            topt = '[' + topt + ']'
        return topt

    def command_usage(command):
        """Get usage text for a command entry."""
        optiontext = ""
        for i in command['args']:
            optiontext += Module.command_single_usage(i) + ' '
        return optiontext.strip()

