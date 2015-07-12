#!/usr/bin/python3
# -*- coding: utf-8 -*-
from imports import *
import configs.locs as locs
import db.text
import signal
import running
import os
import importlib
import time
current_milli_time = lambda: int(round(time.time() * 1000))


def hup_handler(signal, frame):
    print('Reloading from HUP.')
    running.reinit = True


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGHUP, hup_handler)
    except ValueError:
        print('No HUP signal support.')

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
            p = "irc"
            if 'type' in s:
                p = s['type']
            server = importlib.import_module("%s.server" % p).Server(s)
            server.fp = importlib.import_module(
                "%s.fullparse" % p).FullParse
            server.connect()
            running.working_servers.append(server)
        while not running.reinit:
            try:
                for s in configs.servers.servers:
                    p = "irc"
                    if 'type' in s:
                        p = s['type']
                    importlib.import_module('%s' % p).loop()
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
            except InterruptedError:
                pass
            time.sleep(0.05)
        for server in running.working_servers:
            server.reiniting()
        running.working_servers = utils.remove_indices(running.working_servers,
            list(range(len(running.working_servers))))
        moduleregistry.reloadscheduled = True
else:
    raise EnvironmentError('__init__.py must be run as the main!')