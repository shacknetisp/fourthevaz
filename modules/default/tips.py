# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['tips.linedb'] = linedb.LineDB(
        'tip', 'tips', '', 'topic', add, main, remove, showlist, True,
        channel=True)
    ldb = server.state['tips.linedb']
    ldb.initserver(server)
    m = configs.module.Module('tips')
    ldb.configure(m)
    return m


def add(fp, args):
    ldb = fp.server.state['tips.linedb']
    return ldb.add(fp, args, '')


def main(fp, args):
    ldb = fp.server.state['tips.linedb']
    return ldb.main(fp, args, '')


def showlist(fp, args):
    ldb = fp.server.state['tips.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['tips.linedb']
    return ldb.remove(fp, args, '')

