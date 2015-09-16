# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['jokes.linedb'] = linedb.LineDB(
        'joke', 'jokes', server.roomtemplate()[0],
        server.roomtemplate()[1], add, main, remove, showlist, True,
        ' !target! and !joker! are the tokens.', channel=True,
        aname="joke/target", search=False)
    ldb = server.state['jokes.linedb']
    ldb.initserver(server)
    m = configs.module.Module('jokes')
    ldb.configure(m)
    return m


def add(fp, args):
    ldb = fp.server.state['jokes.linedb']
    return ldb.add(fp, args, fp.room(), True)


def main(fp, args):
    ldb = fp.server.state['jokes.linedb']
    r = ldb.main(fp, args, fp.room())
    if 'add' in args.lin or 'remove' in args.lin:
        return r
    return r.replace(
                    '!target!', args.getlinstr(
                        'joke/target', fp.user)).replace(
                            '!joker!', fp.user)


def showlist(fp, args):
    ldb = fp.server.state['jokes.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['jokes.linedb']
    return ldb.remove(fp, args, fp.room(), True)

