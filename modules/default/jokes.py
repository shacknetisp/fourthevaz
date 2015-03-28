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
    server.state['jokes.linedb'] = linedb.LineDB(
        'joke', 'jokes', '#', 'channel', add, main, remove, True,
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
    return ldb.add(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')


def main(fp, args):
    r = ldb.main(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')
    if 'add' in args.lin or 'remove' in args.lin:
        return r
    return r.replace(
                    '!target!', args.getlinstr(
                        'target', fp.sp.sendernick)).replace(
                            '!joker!', fp.sp.sendernick)


def remove(fp, args):
    return ldb.remove(fp, args, fp.channel.entry[
                'channel'] if fp.channel and fp.channel.entry else '')

