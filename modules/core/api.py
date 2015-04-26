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
            options['server'].state[
                    'wserver'] = wsgiref.simple_server.make_server(
                '', options['server'].entry['apiport'],
                application(options['server']))
            print(('Opening API server on %d' % options[
                'server'].entry['apiport']))
    except OSError:
        print(('Unable to open API server on %d' % options[
                'server'].entry['apiport']))
    m.set_help('Access various bot functions from a json API.')
    m.add_timer_hook(1 * 1000, timer)
    m.add_base_hook('apiaction', apiaction)
    return m


class application:

    def __init__(self, server):
        self.server = server

    def __call__(self, environ, start_response):
        ret = {
            'status': 'error',
            'message': 'unknown',
            }
        start_response('200 OK',
                       [('content-type', 'text/html;charset=utf-8')])
        q = parse.parse_qs(environ['QUERY_STRING'])
        action = q['action'][0] if 'action' in q else ''
        try:
            ret['message'] = 'invalid action'
            ret['status'] = 'error'
            self.server.do_base_hook('apiaction',
                ret, self.server, q, environ, action)
        except KeyError:
            pass
        return [json.dumps(ret).encode('utf-8')]


def apiaction(ret, server, q, environ, action):
    if action == 'command':
        del ret['message']

        def process_message(sp):
            fp = irc.fullparse.FullParse(
                server, sp, nomore=True)
            return fp.execute(sp.text)
        ip = environ['REMOTE_ADDR']
        if 'command' not in q:
            ret['message'] = 'no command'
            ret['status'] = 'error'
        ret['output'] = process_message(
            irc.splitparse.SplitParser(
            ':%s!%s PRIVMSG %s :%s' % (':' + ip, "~api@" + ip,
                server.nick,
                q['command'][0],
                )))
        ret['status'] = 'good'


def timer():
    for server in bot.servers():
        if 'wserver' not in server.state:
            continue
        wserver = server.state['wserver']
        inr, _, _ = select.select([wserver], [], [], 0.1)
        if inr:
            wserver.handle_request()