# -*- coding: utf-8 -*-
ctcplist = []
alllist = []
import utils


class Module:

    def __init__(self, name):
        self.base_hooks = {}
        self.command_hooks = {}
        self.timer_hooks = []
        self.helptext = ""
        self.name = name.split('.')[-1]
        self.aliases = {}
        self.rights = []
        self.implicitrights = {}

    def add_implicit_rights(self, d):
        for right in d:
            for implies in [d[right]] if type(d[right]) is str else d[right]:
                if right not in self.implicitrights:
                    self.implicitrights[right] = []
                if implies not in self.implicitrights[right]:
                    self.implicitrights[right].append(implies)

    def add_alias(self, name, content):
        self.aliases[name] = content

    def add_aliases(self, aliases):
        self.aliases = utils.merge_dicts(self.aliases, aliases)

    def add_rights(self, rights):
        self.rights += rights

    def set_help(self, helptext):
        self.helptext = helptext

    def add_base_hook(self, hook, f):
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
        self.timer_hooks.append({
            'time': time,
            'lasttime': 0,
            'function': f,
            })

    def add_command_hook(self, hook, p_d):
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
        args = []
        for arg in argstrs:
            ad = {
                'optional': False,
                'help': arg.split('::')[1],
                'end': False,
                'rights': rights,
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
            })

    def add_command_alias(self, alias, hook):
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
        optiontext = ""
        for i in command['args']:
            optiontext += Module.command_single_usage(i) + ' '
        return optiontext.strip()

