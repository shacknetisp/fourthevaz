# -*- coding: utf-8 -*-
from configs.module import Module
import configs.mload
import running
from . import commands


def init():
    m = Module('aliases')
    m.set_help('Manage aliases.')
    m.add_command_hook('set',
        {
            'function': setalias,
            'help': 'Set aliases.',
            'args': [
                {
                    'name': 'scope',
                    'optional': False,
                    'help': 'Scope of the alias (server, channel).',
                    },
                {
                    'name': 'alias',
                    'optional': False,
                    'help': 'Alias name.',
                    },
                    {
                    'name': 'content',
                    'optional': False,
                    'help': 'Content of the alias.',
                    'end': True,
                    },
                ],
            })
    m.add_command_hook('get',
        {
            'function': get,
            'help': 'Get a list of aliases or the content of a specific alias.',
            'args': [
                    {
                    'name': 'alias',
                    'optional': True,
                    'help': 'Alias name.',
                    },
                ],
            })
    m.add_command_hook('delete',
        {
            'function': delete,
            'help': 'Delete an alias.',
            'args': [
                    {
                    'name': 'alias',
                    'optional': False,
                    'help': 'Alias name.',
                    },
                ],
            })
    m.add_command_hook('alias',
        {
            'function': aliasfunction,
            'help': 'Convenience function, defaults to aliases.get.',
            'args': [
                    {
                    'name': 'set',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Use .set.',
                    },
                    {
                    'name': 'delete',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Use .delete.',
                    },
                    {
                        'name': 'args',
                        'optional': True,
                        'help': 'Arguments.',
                        'end': True,
                        },
                ],
            })
    return m


def delete(fp, args):
    alias = args.getlinstr('alias')
    if fp.channel and alias in fp.channel.aliases:
        content = fp.channel.aliases[alias]
        del fp.channel.aliases[alias]
        return 'Deleted channel alias <%s>: %s' % (alias, content)
    elif alias in fp.server.db['aliases']:
        if fp.serverlevel < 25:
            return 'You must be level 25 or higher to modify aliases.'
        content = fp.server.db['aliases'][alias]
        del fp.server.db['aliases'][alias]
        for server in running.working_servers:
            server.update_aliases()
        return 'Deleted server alias <%s>: %s' % (alias, content)
    else:
        if alias in fp.get_aliases():
            return 'That alias cannot be modified.'
        return 'Non-existent alias.'


def setalias(fp, args):
    scope = args.getlinstr('scope')
    alias = args.getlinstr('alias')
    content = args.getlinstr('content', '')
    if scope == 'channel':
        if alias in fp.server.db['aliases']:
            return 'That alias already exists as a server alias.'
        if not fp.channel:
            return 'You are not in a channel.'
        if fp.accesslevel() < 25:
            return 'You must be level 25 or higher to modify aliases.'
        fp.channel.aliases[alias] = content
        return 'Set channel alias <%s> to: %s' % (alias, content)
    elif scope == 'server':
        if fp.channel and alias in fp.channel.aliases:
            return 'That alias already exists as a channel alias.'
        if fp.serverlevel < 25:
            return 'You must be level 25 or higher to modify aliases.'
        fp.server.db['aliases'][alias] = content
        for server in running.working_servers:
            server.update_aliases()
        return 'Set server alias <%s> to: %s' % (alias, content)
    else:
        return 'Invalid scope.'


def get(fp, args):
    alias = args.getlinstr('alias', '')
    if not alias:
        return commands.doptext(fp, 'list.aliases')
    else:
        try:
            return fp.get_aliases()[alias]
        except KeyError:
            return 'That alias does not exist.'


def aliasfunction(fp, args):
    if 'set' in args.lin:
        return commands.doptext(
            fp, 'aliases.set %s' % args.getlinstr('args', ''))
    elif 'delete' in args.lin:
        return commands.doptext(
            fp, 'aliases.delete %s' % args.getlinstr('args', ''))
    else:
        return commands.doptext(
            fp, 'aliases.get %s' % args.getlinstr('args', ''))

