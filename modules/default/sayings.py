# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['sayings.linedb'] = linedb.LineDB(
        'saying', 'sayings', '#', 'channel', add, main, remove, showlist, True,
        channel=True)
    ldb = server.state['sayings.linedb']
    ldb.initserver(server)
    m = configs.module.Module(__name__)
    ldb.configure(m)
    return m


def add(fp, args):
    ldb = fp.server.state['sayings.linedb']
    c = fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else ''
    return ldb.add(fp, args, c, True)


def main(fp, args):
    ldb = fp.server.state['sayings.linedb']
    c = fp.channel.entry['channel'] if fp.channel and fp.channel.entry else ""
    return ldb.main(fp, args, c)


def showlist(fp, args):
    ldb = fp.server.state['sayings.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['sayings.linedb']
    c = fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else ""
    return ldb.remove(fp, args, c, True)

