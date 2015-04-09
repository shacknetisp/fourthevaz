# -*- coding: utf-8 -*-
import socket
import time
import re
from collections import deque
from . import splitparse
from . import fullparse
import configs.mload as mload
import configs.locs as locs
import moduleregistry
import running
import utils
import ast
moduleregistry.add_module(splitparse)
moduleregistry.add_module(fullparse)
moduleregistry.add_module(mload)
current_milli_time = lambda: int(round(time.time() * 1000))


def encode(inp):
    return inp.encode()


class Server:

    def __init__(
        self, address, port, nick, name, channels, entry, options={
        'print_log': True,
        'tick_min': 50,
        'whois_tick_min': 1000,
        'recv_size': pow(2, 12),
        }):
        if entry['settings'] not in running.serverdb.db():
            running.serverdb.db()[entry['settings']] = {}
        self.db = running.serverdb.db()[entry['settings']]
        self.state = {}
        self.options = options
        self.address = address
        self.port = port
        self.nick = nick
        self.name = name
        self.outputbuffer = deque()
        self.logbuffer = []
        self.lasttick = 0
        self.lastwhoistick = 0
        self.socket = None
        self.entry = entry
        self.channels = []
        for c in channels:
            c = self.shortchannel(c)
            self.channels.append(c)
        self.properties = {}
        self.properties['joined'] = False
        self.modules = []
        self.reinit()
        self.reloaded = False
        self.whoisbuffer = []
        self.whoislist = {}

    def update_aliases(self):
        if 'aliases' not in self.db or type(self.db['aliases']) is not dict:
            self.db['aliases'] = {}
        d = {}
        try:
            d = ast.literal_eval(open(locs.userdata + '/aliases.py').read())
        except FileNotFoundError:
            pass
        self.aliasdb = utils.merge_dicts(
            mload.import_module_py("share.aliases", "core").aliases,
                 mload.import_module_py(
                     "share.aliases", self.entry['moduleset']).aliases, d,
                      self.db['aliases'])
        for m in self.modules:
            self.aliasdb = utils.merge_dicts(self.aliasdb, m.aliases)

    def whois(self, name):
        self.whoisbuffer.append(name)

    def shortchannel(self, c):
        if type(c) is str:
            c = {
            'channel': c,
            'disable': [],
            'prefix': self.entry['prefix'],
            }
        if 'disable' not in c:
            c['disable'] = []
        if 'prefix' not in c:
            c['prefix'] = self.entry['prefix']
        if 'disabled' not in c:
            c['disabled'] = False
        return c

    def reinit(self):
        self.update_aliases()
        mload.serverinit(self)
        self.load_commands()

    def initjoin(self):
        self.do_base_hook('joined', self)
        self.properties['joined'] = True
        for channel in self.channels:
            self.join_channel(channel)

    def join_channel(self, c):
        if 'bot.enable.%s' % self.shortchannel(c)['channel'] not in self.db:
            self.db['bot.enable.%s' % self.shortchannel(c)['channel']] = True
        if self.shortchannel(c)['disabled']:
            self.db['bot.enable.%s' % self.shortchannel(c)['channel']] = False
        self.write_cmd('JOIN ', self.shortchannel(c)['channel'])
        name = self.entry['access'][0] + ':' + self.shortchannel(c)['channel']
        if name not in running.accesslist.db():
            running.accesslist.db()[name] = {}
            running.accesslist.save()
        self.entry['access'].append(name)
        if ('aliases:%s' % self.shortchannel(c)['channel']) not in self.db:
            self.db['aliases:%s' % self.shortchannel(c)['channel']] = {}

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
        self.write_raw(encode(message) + b"\n")

    def write_nocmd(self, text):
        message = text
        self.write_raw(encode(message) + b"\n")

    def setuser(self):
        self.log('Init', 'USER and NICK: %s:%s' % (self.nick, self.name))
        self.write_cmd('USER', '%s 8 * :%s' % (self.nick, self.name))
        self.write_cmd('NICK', self.nick)

    def reconnect(self):
        self.properties['joined'] = False
        self.socket.close()
        self.connect()

    def connect(self):
        try:
            self.state['lastpong'] = time.time()
            self.socket = socket.socket()
            self.log('Init', 'Connecting to %s:%d' % (self.address, self.port))
            self.socket.connect((self.address, self.port))
            self.setuser()
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
            ircmsg = ircmsg.strip('\r')
            ircmsg = regex.sub("", ircmsg)
            self.log('In', ircmsg)
            #Parse Message
            if ircmsg and ircmsg[0] == ':':
                self.process_message(splitparse.SplitParser(ircmsg))

    def get_channel_access(self, galf, fp, channel, ltn=False):
        return galf(
            self, fp.accesslevelname,
            str(self.entry[
                'settings'] + ':' + channel), fp.channel, ltn=ltn)

    def process(self):
        if current_milli_time() - self.lasttick > self.options['tick_min']:
            self.lasttick = current_milli_time()
            if self.outputbuffer:
                out = self.outputbuffer.popleft()
                try:
                    self.socket.send(out)
                except OSError:
                    if self.socket.fileno() < 0:
                        return
                    raise Server.ServerConnectionException(self)
            if self.whoisbuffer and (current_milli_time() -
            self.lastwhoistick > self.options['whois_tick_min']):
                self.lastwhoistick = current_milli_time()
                self.write_cmd('WHOIS', self.whoisbuffer.pop(0))

    def process_message(self, sp):
        if sp.iscode('endmotd') and not self.properties['joined']:
            self.initjoin()
        self.do_base_hook('prerecv', fullparse.FullParse(self, sp))
        self.do_base_hook('recv', fullparse.FullParse(self, sp))

    def do_base_hook(self, name, *args, **kwargs):
        for m in self.modules:
            for f in m.get_base_hook(name):
                try:
                    f(*args, **kwargs)
                except Exception:
                    import traceback
                    print((traceback.format_exc()))

    def load_commands(self):
        self.commands = {}

        def loadcommand(m):
            for k in list(m.command_hooks.keys()):
                v = m.command_hooks[k]
                if k not in self.commands:
                    self.commands[k] = {}
                self.commands[k][m.name] = v
        for m in self.modules:
            loadcommand(m)

    def delete_module(self, name):
        index = -1
        for i in range(len(self.modules)):
            if self.modules[i].name == name:
                index = i
        if index >= 0:
            print(('Removed Module: %s' % name))
            for f in self.modules[index].get_base_hook('unload'):
                f(self)
            del self.modules[index]
            return True
        return False

    def add_module(self, name, mset=""):
        if not mset:
            mset = self.entry['moduleset']
        self.delete_module(name)
        try:
            m = mload.import_module(
                name, mset, options={'server': self})
        except mload.DepException as e:
            print(('Dependancy Exception in %s: %s' % (name, e.e)))
            return
        self.modules.append(m)
        self.update_aliases()
        print(('Added Module: %s' % name))

    class ServerConnectException(Exception):

        def __init__(self, server):
            self.server = server

        def __str__(self):
            return '%s:%d failed to connect.' % (
                self.server.address, self.server.port)

    class ServerConnectionException(Exception):

        def __init__(self, server):
            self.server = server

        def __str__(self):
            return '%s:%d failed to maintain the connection.' % (
                self.server.address, self.server.port)