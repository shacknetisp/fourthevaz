# -*- coding: utf-8 -*-
import base.server
import time
from . import fullparse
import moduleregistry
moduleregistry.add_module(fullparse)
current_milli_time = lambda: int(round(time.time() * 1000))


def encode(inp):
    return inp.encode()


class Server(base.server.Server):

    def __init__(self, entry, options={
        'print_log': True,
        'tick_min': 400,
        'whois_tick_min': 1000,
        'recv_size': pow(2, 12),
        }):
        super(Server, self).__init__(entry, options)
        self.type = 'file'
        """Type of Server"""
        self.file = entry['file']
        """Input File"""
        self.reinit()

    def doline(self, line):
        self.do_base_hook('recv', fullparse.FullParse(self, line))

    def output(self, text):
        print('!!! %s' % text)
