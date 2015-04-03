# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs
ldb = None


def init(options):
    global ldb
    server = options['server']
    linedb = configs.mload.import_module_py("share.linedb", "default")
    server.state['faq.linedb'] = linedb.LineDB(
        'faq', 'faq', '', 'name', add, main, remove, showlist, False)
    ldb = server.state['faq.linedb']
    ldb.initserver(server)
    m = configs.module.Module('faq')
    ldb.configure(m)
    return m


def add(fp, args):
    return ldb.add(fp, args, '')


def main(fp, args):
    return ldb.main(fp, args, '')


def showlist(fp, args):
    return ldb.showlist(fp, args)


def remove(fp, args):
    return ldb.remove(fp, args, '')

