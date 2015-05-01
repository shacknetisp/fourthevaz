# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['quotes.linedb'] = linedb.LineDB(
        'quote', 'quotes', server.roomtemplate()[0],
        server.roomtemplate()[1], add, main, remove, showlist, True,
        channel=True)
    ldb = server.state['quotes.linedb']
    ldb.initserver(server)
    m = configs.module.Module('quotes')
    ldb.configure(m)
    return m


def add(fp, args):
    ldb = fp.server.state['quotes.linedb']
    return ldb.add(fp, args, fp.room(), True)


def main(fp, args):
    ldb = fp.server.state['quotes.linedb']
    return ldb.main(fp, args, fp.room())


def showlist(fp, args):
    ldb = fp.server.state['quotes.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['quotes.linedb']
    return ldb.remove(fp, args, fp.room(), True)

