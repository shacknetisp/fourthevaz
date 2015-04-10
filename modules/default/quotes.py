# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['quotes.linedb'] = linedb.LineDB(
        'quote', 'quotes', '#', 'channel', add, main, remove, showlist, True)
    ldb = server.state['quotes.linedb']
    ldb.initserver(server)
    m = configs.module.Module('quotes')
    ldb.configure(m)
    return m


def add(fp, args):
    ldb = fp.server.state['quotes.linedb']
    c = fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else ''
    return ldb.add(fp, args, c, True)


def main(fp, args):
    ldb = fp.server.state['quotes.linedb']
    c = fp.channel.entry['channel'] if fp.channel and fp.channel.entry else ""
    return ldb.main(fp, args, c)


def showlist(fp, args):
    ldb = fp.server.state['quotes.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['quotes.linedb']
    c = fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else ""
    return ldb.remove(fp, args, c, True)

