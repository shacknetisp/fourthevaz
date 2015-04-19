# -*- coding: utf-8 -*-
import configs.module
import configs.locs
from . import ailib
import time


def init(options):
    server = options['server']
    server.state['ai'] = ailib.AI(
        configs.locs.userdb + '/ailib.%s.py' % server.entry['settings'])
    m = configs.module.Module(__name__)
    m.set_help('Talk with the chatbot.')
    m.add_short_command_hook(chatbot, 'chatbot::Talk to the bot',
        ['text...::What you have to say.'],
        'normal')
    m.add_command_alias('c', 'chatbot')
    m.add_command_alias('talk', 'chatbot')
    return m


def chatbot(fp, args):
    ai = fp.server.state['ai']
    e = 'chatbot.lastphrase.%s' % fp.outtarget()
    etime = e + '.time'
    lasttime = fp.server.state[
        etime] if etime in fp.server.state else time.time()
    lastphrase = fp.server.state[e] if e in fp.server.state else None
    if (time.time() - lasttime) > 30:
        lastphrase = ""
    fp.server.state[
        etime] = time.time()
    out = ai.process(args.getlinstr('text'), lastphrase)
    fp.server.state[e] = out
    return out