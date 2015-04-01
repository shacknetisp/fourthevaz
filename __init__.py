#!/usr/bin/python3
# -*- coding: utf-8 -*-
import irc
import select
import configs
import time
import configs.module as module
import configs.match as match
import configs.mload as mload
import configs.locs as locs
import db.text
import moduleregistry
import running
import os
import utils
import version
import signal
import sys
moduleregistry.add_module(irc)
moduleregistry.add_module(match)
moduleregistry.add_module(utils)
moduleregistry.add_module(module)
moduleregistry.add_module(configs)
moduleregistry.add_module(mload)
moduleregistry.add_module(version)


def signal_handler(signal, frame):
    print('Going down from a signal!')
    sys.exit(0)
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    print('Press Ctrl+C')
    print(('Fourth Evaz %s' % version.versionstr()))
    running.accesslist = db.text.DB(locs.userdata + '/access.py')
    if os.path.exists(running.accesslist.filename):
        running.accesslist.load()
    running.accesslist.save()
    running.serverdb = db.text.DB(locs.userdata + '/serverdb.py')
    if os.path.exists(running.serverdb.filename):
        running.serverdb.load()
    running.serverdb.save()
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