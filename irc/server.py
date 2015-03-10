# -*- coding: utf-8 -*-
import socket
import time
import re
from collections import deque
from . import splitparse
from . import fullparse
import configs.mload as mload
import moduleregistry
moduleregistry.add_module(splitparse)
moduleregistry.add_module(fullparse)
moduleregistry.add_module(mload)
current_milli_time = lambda: int(round(time.time() * 1000))


class Server:

    def __init__(
        self, address, port, nick, name, channels, entry, options={
        'print_log': True,
        'tick_min': 50,
        'recv_size': pow(2, 12),
        }):
        self.options = options
        self.address = address
        self.port = port
        self.nick = nick
        self.name = name
        self.outputbuffer = deque()
        self.logbuffer = []
        self.lasttick = 0
        self.socket = None
        self.entry = entry
        self.channels = []
        for c in channels:
            c = self.shortchannel(c)
            self.channels.append(c)
        self.properties = {}
        self.properties['joined'] = False
        self.modules = []
        mload.serverinit(self)
        self.load_commands()

    def shortchannel(self, c):
        if type(c) is str:
            c = {
            'channel': c,
            'disable': [],
            'prefix': self.entry['prefix'],
            }
        return c

    def initjoin(self):
        self.properties['joined'] = True
        for channel in self.channels:
            self.join_channel(channel)

    def join_channel(self, c):
        self.write_cmd('JOIN ', c['channel'])

    def log(self, prefix, p_text):
        text = prefix + ': ' + p_text
        self.logbuffer.append(text)
        if self.options['print_log']:
            print((text.strip('\n')))

    def write_raw(self, binary):
        self.outputbuffer.append(binary)
        self.log('Out', binary.decode())

    def write_cmd(self, command, text):
        message = command + ' ' + text
        self.write_raw(message.encode('utf-8', 'ignore') + b"\n")

    def write_nocmd(self, text):
        message = text
        self.write_raw(message.encode('utf-8', 'ignore') + b"\n")

    def connect(self):
        try:
            self.socket = socket.socket()
            self.log('Init', 'Connecting to %s:%d' % (self.address, self.port))
            self.socket.connect((self.address, self.port))
            self.log('Init', 'USER and NICK: %s:%s' % (self.nick, self.name))
            self.write_cmd('USER', '%s 8 * :%s' % (self.nick, self.name))
            self.write_cmd('NICK', self.nick)
            self.log('Init', 'Connection succeded.')
        except OSError:
            raise Server.ServerConnectException(self)

    def socketready(self):
        #Get Message
        ircmsg = ""
        try:
            ircmsg = self.socket.recv(self.options['recv_size']).decode()
        except OSError:
            raise Server.ServerConnectionException(self)
        except UnicodeDecodeError:
            pass
        regex = re.compile(
        "\x03(?:\d{1,2}(?:,\d{1,2})?)?", re.UNICODE)
        for ircmsg in ircmsg.strip().split('\n'):
            ircmsg = regex.sub("", ircmsg)
            self.log('In', ircmsg)
            #Parse Message
            self.process_message(splitparse.SplitParser(ircmsg))

    def process(self):
        if current_milli_time() - self.lasttick > self.options['tick_min']:
            self.lasttick = current_milli_time()
            while self.outputbuffer:
                try:
                    out = self.outputbuffer.popleft()
                except OSError:
                    raise Server.ServerConnectionException(self)
                self.socket.send(out)
                break

    def process_message(self, sp):
        if sp.iscode('endmotd') and not self.properties['joined']:
            self.initjoin()
        self.do_base_hook('recv', fullparse.FullParse(self, sp))

    def do_base_hook(self, name, *args, **kwargs):
        for m in self.modules:
            for f in m.get_base_hooks(name):
                f(*args, **kwargs)

    def load_commands(self):
        self.commands = {}
        for m in self.modules:
            for k in list(m.command_hooks.keys()):
                v = m.command_hooks[k]
                if k not in self.commands:
                    self.commands[k] = {}
                self.commands[k][m.name] = v

    class ServerConnectException:

        def __init__(self, server):
            self.server = server

        def __str__(self):
            return '%s:%d failed to connect.' % (
                self.server.address, self.server.port)

    class ServerConnectionException:

        def __init__(self, server):
            self.server = server

        def __str__(self):
            return '%s:%d failed to maintain the connection.' % (
                self.server.address, self.server.port)