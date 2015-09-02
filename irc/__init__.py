# -*- coding: utf-8 -*-
import moduleregistry
from . import server as server
moduleregistry.add_module(server)
from . import utils as utils
moduleregistry.add_module(utils)
import select
import running
import time
current_milli_time = lambda: int(round(time.time() * 1000))


def loop():
    inr = []
    for server in running.working_servers:
        if server.type != 'irc':
            continue
        if server.socket and server.socket.fileno() > 0:
            inr.append(server.socket)
        elif server.socket and server.socket.fileno() < 0:
            try:
                server.connect()
                server.initjoin()
            except type(server).ServerConnectException as e:
                server.connecttimes += 1
                if server.connecttimes > 4:
                    print((str(e)))
                    server.socket = None
    readyr = []
    times = 0
    while (readyr or not times) and times < 5:
        times += 1
        readyr, readyw, readyx = select.select(
            inr, [], [], 0.01)
        for sock in readyr:
            for server in running.working_servers:
                if server.type != 'irc':
                    continue
                if sock == server.socket:
                    try:
                        server.socketready()
                    except type(server).ServerConnectionException:
                        server.socket.close()
        readyr = []
    for server in running.working_servers:
        if server.type != 'irc':
            continue
        server.process()