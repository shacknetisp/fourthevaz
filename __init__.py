#!/usr/bin/python3
# -*- coding: utf-8 -*-
import irc
import select
import configs
import time
import configs.module as module
import configs.mload as mload
import configs.locs as locs
import db.text
import moduleregistry
import running
import os
import utils
moduleregistry.add_module(irc)
moduleregistry.add_module(utils)
moduleregistry.add_module(module)
moduleregistry.add_module(configs)
moduleregistry.add_module(mload)
moduleregistry.add_module(db.text)
if __name__ == '__main__':
    print('Initializing Fourth Evaz')
    running.accesslist = db.text.DB(locs.userdata + '/access.py')
    if os.path.exists(running.accesslist.filename):
        running.accesslist.load()
    running.accesslist.save()
    for s in configs.servers.servers:
        server = irc.server.Server(
            s['address']['host'],
            s['address']['port'],
            s['id']['nick'],
            s['id']['name'],
            s['channels'], s)
        server.connect()
        running.working_servers.append(server)
    while True:
        inr = []
        for server in running.working_servers:
            if server.socket and server.socket.fileno() > 0:
                inr.append(server.socket)
            elif server.socket and server.socket.fileno() < 0:
                try:
                    server.connect()
                    server.initjoin()
                except type(server).ServerConnectException as e:
                    print((str(e)))
                    server.socket = None
        readyr, readyw, readyx = select.select(
            inr, [], [], 0.2)
        for sock in readyr:
            for server in running.working_servers:
                if sock == server.socket:
                    try:
                        server.socketready()
                    except type(server).ServerConnectionException:
                        server.socket.close()
        time.sleep(0.1)
        for server in running.working_servers:
            server.process()
else:
    raise EnvironmentError('__init__.py must be run as the main!')