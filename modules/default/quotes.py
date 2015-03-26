# -*- coding: utf-8 -*-
import db.text
import configs.match
import configs.module
import configs.mload
import configs.locs
import utils
import os
import random
dbfolder = configs.locs.userdata + '/quotes'
os.makedirs(dbfolder, exist_ok=True)


def init(options):
    server = options['server']
    path = "%s/%s.py" % (
        dbfolder, server.entry['settings'])
    server.state['quotes.db'] = db.text.DB(path)
    if os.path.exists(path):
        server.state['quotes.db'].load()
    server.state['quotes.db'].save()
    m = configs.module.Module('quotes')
    m.set_help('Store and retrieve quotes.')
    m.add_command_hook('add',
        {
            'level': 1,
            'function': add,
            'help': 'Add a quote to the database.',
            'args': [
                {
                'name': 'quote',
                'optional': False,
                'help': 'The quote, in this format: [#channel] <quote here>.',
                'end': True,
                }
                ]
            })
    m.add_command_hook('quote',
        {
            'function': quote,
            'help': 'Get a random quote.',
            'args': [
                {
                'name': 'add',
                'optional': True,
                'keyvalue': '',
                'help': 'Alias for quotes.add.',
                },
                    {
                'name': 'remove',
                'optional': True,
                'keyvalue': '',
                'help': 'Alias for quotes.remove.',
                },
                    {
                'name': 'force',
                'optional': True,
                'keyvalue': '',
                'help': '-force option for remove alias.',
                },
                {
                'name': 'quote',
                'optional': True,
                'help': 'The quote, in this format: [#channel] [<search>].',
                'end': True,
                }
                ]
            })
    m.add_command_hook('remove',
        {
            'function': remove,
            'help': 'Remove a quote.',
            'level': 1,
            'args': [
                    {
                'name': 'force',
                'optional': True,
                'keyvalue': '',
                'help': 'Force removal of multiple quotes.',
                },
                {
                'name': 'quote',
                'optional': False,
                'help': 'The quote, in this format: [#channel] [<search>].',
                'end': True,
                }
                ]
            })
    return m


def splitquote(q, c=""):
    channel = c
    quote = q
    if q and q[0] == '#':
        channel = q.split()[0]
        quote = ' '.join(q.split()[1:])
    return (channel, quote)


def add(fp, args):
    quote = args.getlinstr('quote')
    channel, quote = splitquote(quote,
        fp.channel.entry['channel'] if fp.channel and fp.channel.entry else '')
    if channel == "":
        return 'You must specify a channel.'
    if channel not in fp.server.state['quotes.db'].db:
        fp.server.state['quotes.db'].db[channel] = []
    fp.server.state['quotes.db'].db[channel].append(quote)
    fp.server.state['quotes.db'].save()
    return '"%s" has been added to channel %s' % (quote, channel)


def quote(fp, args):
    commands = configs.mload.import_module_py('commands', '', False)
    quote = args.getlinstr('quote', '')
    if 'add' in args.lin:
        return commands.doptext(fp, 'quotes.add %s' % quote)
    elif 'remove' in args.lin:
        return commands.doptext(fp, 'quotes.remove %s%s' % (
            "-force " if 'force' in args.lin else '',
            quote))
    channel, quote = splitquote(quote,
        fp.channel.entry['channel'] if fp.channel and fp.channel.entry else '')
    db = fp.server.state['quotes.db'].db
    if channel not in db or len(db[channel]) == 0:
        return 'There are no quotes for %s' % channel
    choices = []
    for q in db[channel]:
        if configs.match.matchnocase(q, quote, False):
            choices.append(q)
    if not choices:
        return 'No matching quotes found.'
    return random.choice(choices)


def remove(fp, args):
    quote = args.getlinstr('quote', '')
    channel, quote = splitquote(quote,
        fp.channel.entry['channel'] if fp.channel and fp.channel.entry else '')
    db = fp.server.state['quotes.db'].db
    if channel not in db or len(db[channel]) == 0:
        return 'There are no quotes for %s' % channel
    choices = []
    for qi in range(len(db[channel])):
        q = db[channel][qi]
        if configs.match.matchnocase(q, quote, False):
            choices.append(qi)
    if not choices:
        return 'No matching quotes found.'
    if len(choices) > 1 and 'force' not in args.lin:
        return 'More than one quote will be deleted, use -force to delete them.'
    todelete = db[channel][choices[0]]
    db[channel] = utils.remove_indices(db[channel], choices)
    fp.server.state['quotes.db'].save()
    if len(choices) > 1:
        return 'Deleted %d quotes.' % len(choices)
    else:
        return 'Deleted "%s".' % todelete

