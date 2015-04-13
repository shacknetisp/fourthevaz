# -*- coding: utf-8 -*-
import configs.module
import socket
import running
import time
import utils
import select
import irc.splitparse
import irc.fullparse
import re


def init(options):
    options['server'].state['dcc.chat'] = []
    m = configs.module.Module(__name__)
    m.set_help("Transmit and receive DCC communications.")
    m.add_base_hook('whois.done', whois_done)
    m.add_base_hook('ctcp.dcc', ctcp_dcc)
    m.add_timer_hook(200, timer)
    m.add_rights(['nodcc'])
    return m


class DCC:

    def __init__(self, server, address, port, nick, host):
        self.server = server
        self.address = address
        self.port = port
        self.nick = nick
        self.ready = False
        self.time = time.time()
        self.host = host
        self.auth = ''
        self.socket = None

    def socketready(self):
        #Get Message
        ircmsg = ""
        try:
            ircmsg = self.socket.recv(4096).decode()
        except OSError:
            self.ready = False
            self.time = 0
        except UnicodeDecodeError:
            pass
        regex = re.compile(
        "\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
        if ircmsg == '':
            self.socket = None
            return
        for ircmsg in ircmsg.strip().split('\n'):
            ircmsg = ircmsg.strip('\r')
            ircmsg = regex.sub("", ircmsg)
            if ircmsg:
                #Construct a fake PRIVMSG
                self.process_message(irc.splitparse.SplitParser(
                    ':%s!%s PRIVMSG %s :%s' % (self.nick, self.host,
                        self.server.nick,
                        ircmsg
                        )))

    def process_message(self, sp):
        self.server.log('DCC', sp.message)
        self.server.do_base_hook('prerecv', irc.fullparse.FullParse(
            self.server, sp, self))
        self.server.do_base_hook('recv', irc.fullparse.FullParse(
            self.server, sp, self))


def timer():
    for server in running.working_servers:
        index = 0
        tod = []
        sockets = []
        for dcc in server.state['dcc.chat']:
            if not dcc.ready:
                if time.time() - dcc.time > 10:
                    tod.append(index)
            elif not dcc.socket:
                if time.time() - dcc.time > 10:
                    tod.append(index)
            else:
                sockets.append(dcc.socket)
            index += 1
        server.state['dcc.chat'] = utils.remove_indices(
            server.state['dcc.chat'], tod)
        readyr, readyw, readyx = select.select(
                    sockets, [], [], 0.05)
        for sock in readyr:
            for dcc in server.state['dcc.chat']:
                if sock == dcc.socket:
                    dcc.socketready()


def whois_done(server, nick, whois):
    for dcc in server.state['dcc.chat']:
        if not dcc.ready:
            if nick == dcc.nick:
                dcc.auth = whois['authed'] if 'authed' in whois else ''
                dcc.ready = True
                dcc.socket = socket.socket()
                dcc.socket.settimeout(2)
                dcc.socket.connect((dcc.address, dcc.port))
                dcc.socket.settimeout(None)
                server.log('DCC',
                    'Connected to DCC: %s:%d' % (dcc.address, dcc.port))


def ctcp_dcc(fp):
    if (not (fp.hasright('disable') or
    fp.hasright('nodcc'))) or fp.hasright('owner'):
        if len(fp.ctcptext.split()) == 4:
            if (fp.ctcptext.split()[0] == 'CHAT'
            and fp.ctcptext.split()[1]) == 'CHAT':
                fp.server.log('DCC',
                    'Accepted DCC connection from %s (%s:%d)' % (
                        fp.sp.sendernick,
                        fp.ctcptext.split()[2],
                        int(fp.ctcptext.split()[3])))
                fp.server.state['dcc.chat'].append(DCC(
                    fp.server,
                    fp.ctcptext.split()[2],
                    int(fp.ctcptext.split()[3]),
                    fp.sp.sendernick,
                    fp.sp.host
                    ))
                fp.server.whoisbuffer = [
                    fp.sp.sendernick] + fp.server.whoisbuffer
    pass