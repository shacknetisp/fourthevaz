# -*- coding: utf-8 -*-
import configs.module


def init():
    m = configs.module.Module(__name__)
    m.set_help('Get RE version distribution.')
    m.add_command_hook('revers', {'function': revers,
                       'help': 'Get RE version distribution',
                       'args': []})
    return m


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ''


vnames = [(221, 225, '1.4.9')]


def revers(fp, args):
    redflare = fp.server.import_module('redflare.redflare', True)
    rf = redflare.RedFlare('http://redflare.ofthings.net/reports')
    totalservers = {}
    totalplayers = {}
    versions = []
    for server in rf.servers:
        v = find_between_r(server['description'], '[RE', ']').strip()
        if not v:
            v = str(server['version'])
            for vname in vnames:
                if int(server['version']) in range(vname[0], vname[1]):
                    v = vname[2]
        if v not in versions:
            versions.append(v)
        if v not in totalservers:
            totalservers[v] = 0
        if v not in totalplayers:
            totalplayers[v] = 0
        totalservers[v] += 1
        totalplayers[v] += len(server['players'])
    out = []
    for v in reversed(sorted(versions)):
        out.append('%s: %d Server%s/%d Player%s' % (v, totalservers[v],
                   ('s' if totalservers[v] != 1 else ''),
                   totalplayers[v], ('s' if totalplayers[v] != 1 else ''
                   )))
    if not out:
        return 'No results.'
    return ' -- '.join(out)
