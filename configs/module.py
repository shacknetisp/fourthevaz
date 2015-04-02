# -*- coding: utf-8 -*-
ctcplist = []


class Module:

    def __init__(self, name):
        self.base_hooks = {}
        self.command_hooks = {}
        self.timer_hooks = []
        self.helptext = ""
        self.name = name.split('.')[-1]

    def set_help(self, helptext):
        self.helptext = helptext

    def add_base_hook(self, hook, f):
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
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
        d['module'] = self
        d['name'] = hook
        d['haskeyvalue'] = False
        for i in d['args']:
            if 'keyvalue' in i:
                d['haskeyvalue'] = True
        self.command_hooks[hook] = d

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

