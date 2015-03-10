# -*- coding: utf-8 -*-


class Module():

    def __init__(self):
        self.base_hooks = {}

    def add_base_hook(self, hook, function):
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
        self.base_hooks[hook].append(function)

    def get_base_hooks(self, hook):
        if hook not in self.base_hooks:
            self.base_hooks[hook] = []
        return self.base_hooks[hook]

