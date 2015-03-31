# -*- coding: utf-8 -*-
import requests


class RedFlare:

    def __init__(self, url):
        json = requests.get(url).json()
        self.servers = []
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
                }
            for playerName in server['playerNames']:
                serverdata['players'].append(playerName['plain'])
            self.servers.append(serverdata)