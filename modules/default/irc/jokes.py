# -*- coding: utf-8 -*-
import configs.match
import configs.module
import configs.mload
import configs.locs


def init(options):
    server = options['server']
    linedb = server.import_module("share.linedb", True)
    server.state['jokes.linedb'] = linedb.LineDB(
        'joke', 'jokes', '#', 'channel', add, main, remove, showlist, True,
        ' !target! and !joker! are the tokens.')
    ldb = server.state['jokes.linedb']
    ldb.initserver(server)
    m = configs.module.Module('jokes')
    ldb.configure(m)
    for k in list(m.command_hooks.keys()):
        a = m.command_hooks[k]
        if a['name'] == 'joke':
            a['args'] = [{
                'name': 'target',
                'keyvalue': 'name',
                'optional': True,
                'help': 'Target to replace !target!.',
                }] + a['args']
    return m


def add(fp, args):
    ldb = fp.server.state['jokes.linedb']
    return ldb.add(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '', True)


def main(fp, args):
    ldb = fp.server.state['jokes.linedb']
    r = ldb.main(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')
    if 'add' in args.lin or 'remove' in args.lin:
        return r
    return r.replace(
                    '!target!', args.getlinstr(
                        'target', fp.user)).replace(
                            '!joker!', fp.user)


def showlist(fp, args):
    ldb = fp.server.state['jokes.linedb']
    return ldb.showlist(fp, args)


def remove(fp, args):
    ldb = fp.server.state['jokes.linedb']
    return ldb.remove(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '', True)

