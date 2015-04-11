# -*- coding: utf-8 -*-
from configs.module import Module
import utils
import time
import running


def init(options):
    if 'moderator' not in options['server'].state:
        options['server'].state['moderator'] = {}
    m = Module(__name__)
    m.set_help('Moderate channels.')
    m.add_base_hook('recv', recv)
    m.add_timer_hook(10 * 1000, timer)
    m.add_command_hook('enablemoderator', {
        'function': enablemoderator,
        'help': 'Enable moderator in a channel.',
        'level': 50,
        'args': [
            {
                'name': 'enable?',
                'optional': False,
                'help': 'Enable or not.',
                },
            {
                'name': 'channel',
                'optional': True,
                'help': 'Channel to set.'
                }
            ]
        })
    m.add_command_hook('kick', {
        'function': kick,
        'help': 'Kick a nick from the channel.',
        'level': 50,
        'args': [
            {
                'name': 'nick',
                'optional': False,
                'help': 'Nick to kick.',
                },
            {
                'name': 'msg',
                'optional': True,
                'help': 'Message to send.',
                },
            ]
        })
    m.add_command_hook('ban', {
        'function': ban,
        'help': "Ban a nick from the channel.",
        'level': 50,
        'args': [
            {
                'name': 'nick',
                'optional': False,
                'help': 'Nick to ban.',
                },
            ]
        })
    m.add_alias('kickban',
        'absorb "Attempted to kickban $1" <kick $1 $*><ban $1>')
    return m


def timer():
    for server in running.working_servers:
        db = server.state['moderator']
        for p in db:
            if time.time() - db[p]['lastmessage'] > 10:
                db[p]['lastmessagetext'] = ''
                if db[p]['evilness'] > 0:
                    db[p]['evilness'] -= 1
                elif db[p]['kicks'] > 0:
                    db[p]['kicks'] -= 1


def enablemoderator(fp, args):
    if not fp.channel and 'channel' not in args.lin:
        return 'You are not calling from a channel.'
    channel = fp.channel.entry[
        'channel'] if fp.channel else args.getlinstr('channel')
    try:
        fp.server.db[
            'moderator.enable.%s' % channel] = utils.boolstr(
                args.getlinstr('enable?'))
        return ('Enabled in %s: ' % channel) + str(
            fp.server.db['moderator.enable.%s' % fp.channel.entry['channel']])
    except ValueError as e:
        return str(e)


def getcharacterrepition(s):
    if not s:
        return 0
    total = len(s)
    highest = 0
    tried = []
    for c in s:
        if c not in tried:
            tried.append(c)
            highest = max(highest, s.count(c))
    return (highest / total) * 100


def recv(fp):
    if fp.sp.iscode('chat') and fp.channel:
        if not fp.server.db[
            'bot.enable.%s' % fp.channel.entry['channel']]:
            return
        db = fp.server.state['moderator']
        rfes = 'moderator.enable.%s' % fp.channel.entry['channel']
        if not rfes in fp.server.db or not fp.server.db[rfes]:
            return
        if fp.sp.sendernick:
            if fp.accesslevel() >= 50:
                return
            if fp.external():
                return
            if fp.sp.sendernick not in db:
                db[fp.sp.sendernick] = {
                    'lastmessage': time.time(),
                    'lastmessagetext': fp.sp.text,
                    'evilness': 0,
                    'kicks': 0,
                    }
            if time.time() - db[fp.sp.sendernick]['lastmessage'] < 2 or (
                db[fp.sp.sendernick]['lastmessagetext'] == fp.sp.text
                ):
                db[fp.sp.sendernick]['evilness'] += 1
            elif getcharacterrepition(fp.sp.text) > 40 and len(fp.sp.text) > 10:
                db[fp.sp.sendernick]['evilness'] += 2
            elif time.time() - db[fp.sp.sendernick]['lastmessage'] > 3:
                if db[fp.sp.sendernick]['evilness'] > 0:
                    db[fp.sp.sendernick]['evilness'] -= 1
            if db[fp.sp.sendernick]['evilness'] == 2:
                fp.reply('%s: Stop spamming.' % fp.sp.sendernick)
            if db[fp.sp.sendernick][
                'evilness'] >= (4 if fp.accesslevel() < 25 else 6):
                fp.server.write_cmd(
                    'KICK', '%s %s :Do not spam. %s' % (
                        fp.channel.entry['channel'],
                        fp.sp.sendernick,
                        'You will be banned soon!' if db[
                            fp.sp.sendernick]['kicks'] == 1 else
                            'Use http://0bin.net/ or another pastebin ' +
                            'service if necessary.'
                        ))
                #Give a change to repent
                db[fp.sp.sendernick]['evilness'] -= 1
                if fp.accesslevel() < 25:
                    db[fp.sp.sendernick]['evilness'] -= 2
                db[fp.sp.sendernick]['kicks'] += 1
                if db[fp.sp.sendernick]['kicks'] > 2:
                    fp.server.write_cmd(
                        'MODE', '%s +b *!*@%s' % (
                            fp.channel.entry['channel'],
                            fp.sp.sender.split('@')[1],
                            ))
            db[fp.sp.sendernick]['lastmessage'] = time.time()
            db[fp.sp.sendernick]['lasttext'] = fp.sp.text


def kick(fp, args):
    if not fp.channel:
        return 'You are not in a channel.'
    fp.server.write_cmd('KICK', '%s %s :%s' % (
        fp.channel.entry['channel'],
        args.getlinstr('nick'),
        args.getlinstr('msg', ''),
        ))
    return 'Attempted to kick %s' % args.getlinstr('nick')


def ban(fp, args):
    if not fp.channel:
        return 'You are not in a channel.'
    try:
        host = fp.server.whoislist[args.getlinstr('nick')]['host']
    except KeyError:
        return "I don't have information about %s." % args.getlinstr('nick')
    fp.server.write_cmd(
        'MODE', '%s +b *!*@%s' % (
            fp.channel.entry['channel'],
            host,
            ))
    return 'Attempted to ban %s.' % args.getlinstr('nick')
