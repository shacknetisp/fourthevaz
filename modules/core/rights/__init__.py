# -*- coding: utf-8 -*-
from configs.module import Module
import importlib
from . import access
import fnmatch
importlib.reload(access)
import utils


def init():
    m = Module('rights')
    m.set_help('Manage user rights.')
    m.add_command_hook('getrights',
        {
            'function': getrights,
            'help': 'Get user rights.',
            'args': [
                {
                    'name': 'base',
                    'keyvalue': '',
                    'optional': True,
                    'help': 'Only show base rights.',
                    },
                {
                    'name': 'user',
                    'optional': True,
                    'help': 'The user to view, defaults to caller. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                {
                    'name': 'rights',
                    'optional': True,
                    'help': 'Rights to test.'
                    }
                ],
            })
    m.add_command_hook('addrights',
        {
            'function': addrights,
            'help': 'Add user rights.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to set. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                        {
                    'name': 'rights',
                    'optional': False,
                    'end': True,
                    'help': 'The rights to set.'
                    },
                ],
            })
    m.add_command_hook('delrights',
        {
            'function': delrights,
            'help': 'Delete user rights.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to set. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                        {
                    'name': 'rights',
                    'optional': False,
                    'end': True,
                    'help': 'The rights to set.'
                    },
                ],
            })
    m.add_command_hook('getusers',
        {
            'function': getusers,
            'help': 'Get a list of users matching a "regex".',
            'args': [
                {
                    'name': 'search',
                    'optional': False,
                    'help': 'The "regex" to search for, uses fnmatchcase().'
                    },
                ],
            })
    m.add_command_hook('listrights',
        {
            'function': listrights,
            'help': 'Get a list of all rights.',
            'args': [],
            })
    m.add_rights([
        'disable',
        '%,disable',
        'admin',
        'owner',
        'normal',
        '%,normal',
        '%,op',
        '%,voice',
        ])
    m.add_implicit_rights(
        {
            '%,op': '%,normal',
            '%,voice': '%,normal',
            'admin': ['%,normal', 'normal'],
            'owner': 'admin',
        })
    m.add_command_alias('setrights', 'addrights')
    m.add_command_alias('removerights', 'delrights')
    m.add_base_hook('whois.done', whois_done)
    return m


def whois_done(server, nick, whois):
    access = server.import_module('rights.access', False)
    rights = access.getrights(server, "%s=%s@%s=%s" % (
        nick, whois['ident'], whois['host'],
        whois['authed'] if 'authed' in whois else ''))
    for c in whois['channels']:
        if (c + ',op') in rights and c not in whois['op']:
            server.write_cmd('MODE', '%s +o %s' % (c, nick))
        elif (c + ',voice') in rights and c not in whois['voice']:
            server.write_cmd('MODE', '%s +v %s' % (c, nick))


def listrights(fp, args):
    r = []
    for m in fp.server.modules:
        r += m.rights
    return utils.ltos(sorted(r, key=lambda x: x.strip('%,')))


def getusers(fp, args):
    search = args.getlinstr('search')
    try:
        access.raiseifnotformeduser(search)
    except access.AccessLevelError:
        return "Malformed user!"
    results = []
    for user in fp.server.adb:
        if fnmatch.fnmatchcase(user, search):
            results.append(user)
    return('Results: %s' % (utils.ltos(results)))


def getrights(fp, args):
    user = args.getlinstr('user', fp.accesslevelname)
    if user == '.':
        user = fp.accesslevelname
    try:
        access.raiseifnotformeduser(user)
    except access.AccessLevelError:
        return "Malformed user!"
    extra = []
    if fp.type == 'irc':
        for c in fp.server.channels:
            try:
                extra += fp.channelrights('='.join(user.split('=')[:-2]), c)
            except IndexError:
                pass
    if 'base' not in args.lin or args.getlinstr('rights', ''):
        r = access.fullrights(fp, access.getrights(fp.server, user)
        + extra)
    else:
        r = access.getrights(fp.server, user)
    if args.getlinstr('rights', ''):
        hasrights = True
        for right in args.getlinstr('rights', '').split(' '):
            if right not in r:
                hasrights = False
        return "Yes" if hasrights else "No"
    return user + ': ' + utils.ltos(sorted(
        utils.unique(r,
        ), key=lambda x: x.strip('#-')), '; ')


def rightexists(fp, right):
    r = []
    for m in fp.server.modules:
        r += m.rights
    if len(right.split(',')) == 2:
        if '%,' + right.split(',')[1].strip('-') in r:
            return True
        r = right.split(',')[1].strip('-')
    if right.find(':') == 0:
        return True
    elif right in r:
        return True
    else:
        return False


def addrights(fp, args):
    user = args.getlinstr('user')
    try:
        access.raiseifnotformeduser(user)
    except access.AccessLevelError:
        return "Malformed user!"
    finished = []
    for right in args.getlinstr('rights').split(' '):
        sright = right.strip('-')
        if not rightexists(fp, sright):
            return 'That right does not exist.'
        if sright == 'owner':
            return 'You may not set owner.'
        elif sright == 'admin' and not fp.hasright('owner'):
            return 'You may not set admin.'
        channel = "#"
        if access.ischannel(user):
            channel = user
        elif len(right.split(',')) == 2:
            channel = right.split(',')[0]
        if not (fp.hasright('owner')):
            if channel != '#' and not fp.hasright(channel + ',op'):
                return (
                    '%s: You must be either an owner or operator.' % (
                        right))
            elif channel == '#' and not fp.hasright('admin'):
                return (
                    '%s: You must be either an owner or admin.' % (
                        right))
        access.setright(fp.server, user, right)
        finished.append(right)
    return '%s added to %s' % (utils.ltos(finished, '; '), user)


def delrights(fp, args):
    user = args.getlinstr('user')
    try:
        access.raiseifnotformeduser(user)
    except access.AccessLevelError:
        return "Malformed user!"
    finished = []
    for right in args.getlinstr('rights').split(' '):
        sright = right.strip('-')
        if not rightexists(fp, sright):
            return 'That right does not exist.'
        if sright == 'owner':
            return 'You may not set owner.'
        elif sright == 'admin' and not fp.hasright('owner'):
            return 'You may not set admin.'
        channel = "#"
        if access.ischannel(user):
            channel = user
        elif len(right.split(',')) == 2:
            channel = right.split(',')[0]
        if not (fp.hasright('owner')):
            if channel != '#' and not fp.hasright(channel + ',op'):
                return (
                    '%s: You must be either an owner or operator.' % (
                        right))
            elif channel == '#' and not fp.hasright('admin'):
                return (
                    '%s: You must be either an owner or admin.' % (
                        right))
        access.delright(fp.server, user, right)
        finished.append(right)
    return '%s removed from %s' % (utils.ltos(finished, '; '), user)

