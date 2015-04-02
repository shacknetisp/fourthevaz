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
            ]
        })
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
    if not fp.channel:
        return 'You are not calling from a channel.'
    try:
        fp.server.db[
            'moderator.enable.%s' % fp.channel.entry[
                'channel']] = utils.boolstr(
                args.getlinstr('enable?'))
        return 'Enabled: ' + str(
            fp.server.db['moderator.enable.%s' % fp.channel.entry['channel']])
    except ValueError as e:
        return str(e)


def recv(fp):
    if fp.sp.iscode('chat') and fp.channel:
        db = fp.server.state['moderator']
        rfes = 'moderator.enable.%s' % fp.channel.entry['channel']
        if not rfes in fp.server.db or not fp.server.db[rfes]:
            return
        if fp.sp.sendernick:
            if fp.accesslevel() >= 50:
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
            else:
                if db[fp.sp.sendernick]['evilness'] > 0:
                    db[fp.sp.sendernick]['evilness'] -= 1
            if db[fp.sp.sendernick]['evilness'] == 2:
                fp.reply('%s: Stop spamming.' % fp.sp.sendernick)
            if db[fp.sp.sendernick]['evilness'] >= 4:
                fp.server.write_cmd(
                    'KICK', '%s %s :Your evilness is too much for me.' % (
                        fp.channel.entry['channel'],
                        fp.sp.sendernick,
                        ))
                db[fp.sp.sendernick]['kicks'] += 1
                if db[fp.sp.sendernick]['kicks'] > 2:
                    fp.server.write_cmd(
                        'MODE', '%s +b *!*@%s' % (
                            fp.channel.entry['channel'],
                            fp.sp.sender.split('@')[1],
                            ))
            db[fp.sp.sendernick]['lastmessage'] = time.time()
            db[fp.sp.sendernick]['lasttext'] = fp.sp.text
