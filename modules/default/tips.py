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
    server.state['tips.linedb'] = linedb.LineDB(
        'tip', 'tips', '', 'topic', add, main, remove, True)
    ldb = server.state['tips.linedb']
    ldb.initserver(server)
    m = configs.module.Module('tips')
    ldb.configure(m)
    return m


def add(fp, args):
    return ldb.add(fp, args, '')


def main(fp, args):
    return ldb.main(fp, args, '')


def remove(fp, args):
    return ldb.remove(fp, args, '')

