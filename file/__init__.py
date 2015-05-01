# -*- coding: utf-8 -*-
import moduleregistry
from . import server as server
moduleregistry.add_module(server)
import os
import running


def loop():
    for server in running.working_servers:
        if server.type != 'file':
            continue
        if os.path.exists(server.file):
            with open(server.file, 'r') as f:
                for line in f.readlines():
                    server.doline(line)
            os.unlink(server.file)