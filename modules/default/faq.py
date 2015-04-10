# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['faq.linedb'] = linedb.LineDB(
        'faq', 'faq', '', 'name', add, main, remove, showlist, False)
    ldb = server.state['faq.linedb']
    ldb.initserver(server)
    m = configs.module.Module('faq')
    ldb.configure(m)
    return m


def add(fp, args):
    ldb = fp.server.state['faq.linedb']
    return ldb.add(fp, args, '')


def main(fp, args):
    ldb = fp.server.state['faq.linedb']
    return ldb.main(fp, args, '')


def showlist(fp, args):
    ldb = fp.server.state['faq.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['faq.linedb']
    return ldb.remove(fp, args, '')

