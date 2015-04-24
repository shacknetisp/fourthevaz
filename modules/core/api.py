# -*- coding: utf-8 -*-
import configs.module
import wsgiref.simple_server
import select
import json
import bot
from urllib import parse
import irc.fullparse
import irc.splitparse


def init(options):
    m = configs.module.Module(__name__)
    if 'wserver' in options['server'].state:
        del options['server'].state['wserver']
    try:
        if 'apiport' in options['server'].entry:
            try:
                options['server'].state[
                        'wserver'] = wsgiref.simple_server.make_server(
                    '', options['server'].entry['apiport'],
                    application(options['server']))
            except TypeError:
                options['server'].state[
                    'wserver'] = wsgiref.simple_server.make_server(
                0, options['server'].entry['apiport'],
                application(options['server']))
            print(('Opening API server on %d' % options[
                'server'].entry['apiport']))
    except OSError:
        print(('Unable to open API server on %d' % options[
                'server'].entry['apiport']))
    m.set_help('Access various bot functions from a json API.')
    m.add_timer_hook(1 * 1000, timer)
    return m


class application:

    def __init__(self, server):
        self.server = server

    def process_message(self, sp):
        fp = irc.fullparse.FullParse(
            self.server, sp, nomore=True)
        return fp.execute(sp.text)

    def __call__(self, environ, start_response):
        ret = {
            'status': 'error',
            'message': 'unknown',
            }
        start_response('200 OK',
                       [('content-type', 'text/html;charset=utf-8')])
        q = parse.parse_qs(environ['QUERY_STRING'])
        action = q['action'][0] if 'action' in q else ''
        ip = environ['REMOTE_ADDR']
        try:
            if action == 'info':
                del ret['message']
                ret['addr'] = self.server.entry['address']
                ret['channels'] = [
                    c['channel'] for c in self.server.channels]
                ret['nicks'] = [
                    name
                    for c in self.server.channels
                    for name in c['names']
                    ]
                ret['modules'] = [
                (m.name, m.set)
                for m in self.server.modules
                ]
                ret['status'] = 'good'
            elif action == 'command':
                if 'command' not in q:
                    ret['message'] = 'no command'
                    ret['status'] = 'error'
                ret['output'] = self.process_message(
                    irc.splitparse.SplitParser(
                    ':%s!%s PRIVMSG %s :%s' % (':' + ip, "~api@" + ip,
                        self.server.nick,
                        q['command'][0],
                        )))
                ret['status'] = 'good'
            else:
                ret['message'] = 'invalid action'
                ret['status'] = 'error'
        except KeyError:
            pass
        return [json.dumps(ret).encode('utf-8')]


def timer():
    for server in bot.servers():
        if 'wserver' not in server.state:
            continue
        wserver = server.state['wserver']
        inr, _, _ = select.select([wserver], [], [], 0.1)
        if inr:
            wserver.handle_request()