#!/usr/bin/python3
# -*- coding: utf-8 -*-
from imports import *
import select
import time
import configs.locs as locs
import db.text
import signal
import sys
import running
import os


current_milli_time = lambda: int(round(time.time() * 1000))


def signal_handler(signal, frame):
    print('Going down from a signal!')
    sys.exit(0)


def hup_handler(signal, frame):
    print('Reloading from HUP.')
    running.reinit = True


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGHUP, hup_handler)

    print(('Fourth Evaz %s' % version.versionstr()))
    while True:
        running.reinit = False
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
        while not running.reinit:
            try:
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
                did = []
                for server in running.working_servers:
                    for m in server.modules:
                        if m.name not in did:
                            did.append(m.name)
                            for t in m.timer_hooks:
                                if current_milli_time() - t[
                                    'lasttime'] > t['time']:
                                    t['lasttime'] = current_milli_time()
                                    try:
                                        t['function']()
                                    except Exception:
                                        import traceback
                                        print((traceback.format_exc()))
                for server in running.working_servers:
                    server.process()
            except InterruptedError:
                pass
        for server in running.working_servers:
            if server.socket:
                server.socket.send(b"QUIT :I'll be back soon!\n")
                server.socket.close()
        running.working_servers = utils.remove_indices(running.working_servers,
            list(range(len(running.working_servers))))
        moduleregistry.reloadscheduled = True
else:
    raise EnvironmentError('__init__.py must be run as the main!')