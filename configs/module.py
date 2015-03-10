# -*- coding: utf-8 -*-


class Module():

    def __init__(self, name):
        self.base_hooks = {}
        self.command_hooks = {}
        self.helptext = ""
        self.name = name

    def set_help(self, helptext):
        self.helptext = helptext

    def add_base_hook(self, hook, function):
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
        self.base_hooks[hook].append(function)

    def get_base_hooks(self, hook):
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
        return self.base_hooks[hook]

    def add_command_hook(self, hook, d):
        self.command_hooks[hook] = d

