# -*- coding: utf-8 -*-
import irc
import select
import configs
import time
import configs.module as module
import configs.mload as mload
import moduleregistry
import running
moduleregistry.add_module(irc)
moduleregistry.add_module(module)
moduleregistry.add_module(configs)
moduleregistry.add_module(mload)
if __name__ == '__main__':
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
            if server.socket:
                inr.append(server.socket)
        readyr, readyw, readyx = select.select(
            inr, [], [], 0.2)
        for sock in readyr:
            for server in running.working_servers:
                if sock == server.socket:
                    server.socketready()
        time.sleep(0.1)
        for server in running.working_servers:
            server.process()