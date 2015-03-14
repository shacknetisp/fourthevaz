# -*- coding: utf-8 -*-
from configs.module import Module
import importlib
from . import access
import fnmatch
importlib.reload(access)
import running


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
                    {
                    'name': 'accesslist',
                    'optional': True,
                    'keyvalue': 'accesslist',
                    'help': 'The access list to get.'
                    },
                ],
            })
    m.add_command_hook('setrights',
        {
            'function': setrights,
            'help': 'Set user rights.',
            'args': [
                {
                    'name': 'user',
                    'optional': False,
                    'help': 'The user to set. ([<nick>]:'
                    '[<hostname>]:[<NickServ Account>])'
                    },
                        {
                    'name': 'level',
                    'optional': False,
                    'help': 'The access level to set.'
                    },
                        {
                    'name': 'accesslist',
                    'optional': True,
                    'help': 'The access list to set.'
                    }
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
                    {
                    'name': 'accesslist',
                    'optional': True,
                    'keyvalue': 'accesslist',
                    'help': 'The access list to get.'
                    },
                ],
            })
    m.add_command_hook('accesslists',
        {
            'function': accesslists,
            'help': 'Show the access lists.',
            'args': [],
            })
    return m


def accesslists(fp, args):
    fp.reply(str(fp.server.entry['access']))


def getusers(fp, args):
    search = args.getlinstr('search')
    if len(search.split(':')) != access.accesslen:
        fp.reply('Malformed: %s' % search)
        return
    alist = args.getlinstr('accesslist', fp.server.entry['access'][0])
    results = []
    if alist not in running.accesslist.db:
        fp.reply('Invalid Access List.')
        return
    for user in running.accesslist.db[alist]:
        if fnmatch.fnmatchcase(user, search):
            results.append(user)
    fp.reply('%s: %s' % (alist, results))


def getrights(fp, args):
    user = args.getlinstr('user', fp.accesslevelname)
    alist = args.getlinstr('accesslist', '')
    try:
        fp.reply('%s%shas an access level of %d.' % (
            user, ' (' + alist + ') ' if alist else '', access.getaccesslevel(
            fp.server, user, alist)))
    except access.AccessLevelError as e:
        fp.reply(e.msg)


def setrights(fp, args):
    user = args.getlinstr('user')
    alist = args.getlinstr('accesslist', fp.server.entry['access'][0])
    try:
        level = int(args.getlinstr('level'))
    except ValueError:
        fp.reply('Invalid level.')
        return
    required = max(access.getaccesslevel(
            fp.server, user, alist), level) + (
                10 if 'leveladd' not in fp.server.entry else int(
                fp.server.entry['leveladd']))
    sl = access.getaccesslevel(
            fp.server, fp.accesslevelname)
    if sl < required:
        fp.reply('You are level %d, but you need at least level %d.' % (
            sl,
            required
            ))
        return
    try:
        access.setaccesslevel(alist, user, level)
        fp.reply(
            'The access level of %s (%s) is now %d.' % (
                user, alist, access.getaccesslevel(
            fp.server, user)))
    except access.AccessLevelError as e:
        fp.reply(e.msg)

