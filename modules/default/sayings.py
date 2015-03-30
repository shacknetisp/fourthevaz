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
    server.state['sayings.linedb'] = linedb.LineDB(
        'saying', 'sayings', '#', 'channel', add, main, remove, True)
    ldb = server.state['sayings.linedb']
    ldb.initserver(server)
    m = configs.module.Module(__name__)
    ldb.configure(m)
    return m


def add(fp, args):
    c = fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else ''
    return ldb.add(fp, args, c, True)


def main(fp, args):
    c = fp.channel.entry['channel'] if fp.channel and fp.channel.entry else ""
    return ldb.main(fp, args, c)


def remove(fp, args):
    c = fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else ""
    return ldb.remove(fp, args, c, True)

