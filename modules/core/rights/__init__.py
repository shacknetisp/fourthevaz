# -*- coding: utf-8 -*-
from configs.module import Module
import importlib
from . import access
import fnmatch
importlib.reload(access)
import running
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
                    'name': 'user',
                    'optional': True,
                    'help': 'The user to view, defaults to caller. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                ],
            })
    m.add_command_hook('setright',
        {
            'function': setright,
            'help': 'Set a user right.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to set. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                        {
                    'name': 'right',
                    'optional': False,
                    'help': 'The right to set.'
                    },
                ],
            })
    m.add_command_hook('delright',
        {
            'function': delright,
            'help': 'Delete a user right.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to set. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                        {
                    'name': 'right',
                    'optional': False,
                    'help': 'The right to set.'
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
        'admin',
        'owner',
        'normal',
        '%,op',
        '%,voice',
        '%,ignore',
        ])
    return m


def listrights(fp, args):
    r = []
    for m in fp.server.modules:
        r += m.rights
    return utils.ltos(r)


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
    try:
        access.raiseifnotformeduser(user)
    except access.AccessLevelError:
        return "Malformed user!"
    return user + ': ' + utils.ltos(access.getrights(fp.server, user) +
    fp.channelrights())


def setright(fp, args):
    user = args.getlinstr('user')
    right = args.getlinstr('right')
    sright = right.strip('-')
    try:
        access.raiseifnotformeduser(user)
    except access.AccessLevelError:
        return "Malformed user!"
    if sright == 'owner':
        return 'You may not set owner.'
    elif sright == 'admin' and not fp.hasright('owner'):
        return 'You may not set admin.'
    access.setright(fp.server, user, right)
    return '%s given to %s' % (right, user)


def delright(fp, args):
    user = args.getlinstr('user')
    right = args.getlinstr('right')
    sright = right.strip('-')
    try:
        access.raiseifnotformeduser(user)
    except access.AccessLevelError:
        return "Malformed user!"
    if sright == 'owner':
        return 'You may not set owner.'
    elif sright == 'admin' and not fp.hasright('owner'):
        return 'You may not set admin.'
    access.delright(fp.server, user, right)
    return '%s taken from %s' % (right, user)

