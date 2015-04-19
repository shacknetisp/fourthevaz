# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module(__name__)
    m.set_help('Join and part channels.')
    m.add_command_hook('join',
        {
            'function': join,
            'rights': ['admin'],
            'help': 'Join channel.',
            'args': [
                {
                    'name': 'channel',
                    'optional': False,
                    'help': 'Channel to join.',
                    },
                ],
            })
    m.add_command_hook('part',
        {
            'function': part,
            'rights': ['admin'],
            'help': 'Part channel.',
            'args': [
                {
                    'name': 'channel',
                    'optional': True,
                    'help': 'Channel to join.',
                    },
                ],
            })
    return m


def join(fp, args):
    channel = args.getlinstr('channel')

    for c in fp.server.channels:
        if c['channel'] == channel:
            fp.server.write_cmd('PART', fp.server.shortchannel(c)['channel'])
            fp.server.write_cmd('JOIN', fp.server.shortchannel(c)['channel'])
            return "Attempted to rejoin %s" % channel

    fp.server.channels.append(fp.server.shortchannel(channel))
    fp.server.join_channel(channel)
    return "Attempted to join %s" % channel


def part(fp, args):
    channel = args.getlinstr('channel')
    ch = False
    if fp.channel and channel == fp.channel.entry['channel']:
        ch = True

    for i in range(len(fp.server.channels)):
        c = fp.server.channels[i]
        if c['channel'] == channel:
            del fp.server.channels[i]
            fp.server.write_cmd('PART', fp.server.shortchannel(c)['channel'])
            if ch:
                fp.replypriv('Parted %s' % channel)
                return
            else:
                return 'Parted %s' % channel