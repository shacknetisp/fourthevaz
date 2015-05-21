# -*- coding: utf-8 -*-
import requests


class RedFlare:

    def __init__(self, url, timeout=10):
        json = requests.get(url, timeout=timeout).json()
        self.servers = []
        self.players = []
        for serverkey in json:
            server = json[serverkey]
            serverdata = {
                'host': server['host'],
                'port': server['port'],
                'mode': server['gameMode'],
                'mutators': server['mutators'],
                'time': server['timeLeft'],
                'map': server['mapName'],
                'version': server['gameVersion'],
                'description': server['description'],
                'players': [],
                'playerauths': [],
                }
            index = 0
            for playerName in server['playerNames']:
                serverdata['players'].append(playerName['plain'])
                try:
                    serverdata['playerauths'].append([playerName['plain'],
                        server['authNames'][index]['plain']])
                except KeyError:
                    pass
                self.players.append(playerName['plain'])
                index += 1
            self.servers.append(serverdata)