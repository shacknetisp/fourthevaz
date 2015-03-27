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
    server.state['quotes.linedb'] = linedb.LineDB(
        'quote', 'quotes', '#', 'channel', add, main, remove, True)
    ldb = server.state['quotes.linedb']
    ldb.initserver(server)
    m = configs.module.Module('quotes')
    ldb.configure(m)
    return m


def add(fp, args):
    return ldb.add(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')


def main(fp, args):
    return ldb.main(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')


def remove(fp, args):
    return ldb.remove(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')

