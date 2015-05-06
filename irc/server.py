# -*- coding: utf-8 -*-
import base.server
import socket
import re
import time
from collections import deque
from irc import splitparse
from irc import fullparse
import moduleregistry
moduleregistry.add_module(splitparse)
moduleregistry.add_module(fullparse)
current_milli_time = lambda: int(round(time.time() * 1000))


def encode(inp):
    return inp.encode()


class Server(base.server.Server):

    def __init__(self, entry, options={
        'print_log': True,
        'tick_min': 400,
        'whois_tick_min': 1000,
        'recv_size': pow(2, 12),
        }):
        super(Server, self).__init__(entry, options)
        self.type = 'irc'
        """Type of Server"""
        self.address = entry['address']['host']
        """IRC Server IP/Host"""
        self.port = entry['address']['port']
        """IRC Server Port"""
        self.nick = entry['id']['nick']
        """IRC Nick"""
        self.name = entry['id']['name']
        self.outputbuffer = deque()
        self.lasttick = 0
        self.lastwhoistick = 0
        self.socket = None
        self.ssl = ''
        if 'ssl' in entry:
            self.ssl = entry['ssl']
        self.channels = []
        """Current channels."""
        for c in entry['channels']:
            c = self.shortchannel(c)
            self.channels.append(c)
        self.whoisbuffer = []
        """List of nicks to run WHOIS on next."""
        self.whoislist = {}
        """WHOIS information list."""
        self.auth = entry['auth'] if 'auth' in entry else None
        """Tuple for auth: (<type>, [<account>] or "", <password>)."""
        self.connecttimes = 0
        self.properties['joined'] = False
        self.reinit()

    def roomtemplate(self):
        """Return the room template."""
        return ("#", "channel")

    def whois(self, name, queue=True):
        """
        Add <name> to the WHOIS buffer.
        If queue, add to the end, otherwise add to the front.
        """
        self.log('WHOIS', "%s = %d" % (name,
        len(self.whoisbuffer) + 1))
        if not queue:
            self.whoisbuffer = [name] + self.whoisbuffer
            return
        self.whoisbuffer.append(name)

    def shortchannel(self, c):
        if type(c) is str:
            c = {
            'channel': c,
            'prefix': self.entry['prefix'],
            }
        if 'prefix' not in c:
            c['prefix'] = self.entry['prefix']
        return c

    def initjoin(self):
        self.do_base_hook('joined', self)
        self.properties['joined'] = True
        if not self.auth:
            self.join_channels()

    def join_channels(self):
        for channel in self.channels:
            self.join_channel(channel)

    def join_channel(self, c):
        """JOIN <c> and make the alias database."""
        self.write_cmd('JOIN ', self.shortchannel(c)['channel'])
        if ('aliases:%s' % self.shortchannel(c)['channel']) not in self.db:
            self.db['aliases:%s' % self.shortchannel(c)['channel']] = {}

    def flush(self):
        """Flush the output buffer before the process loop."""
        while self.outputbuffer:
            if current_milli_time() - self.lasttick > self.options[
                'tick_min']:
                    self.lasttick = current_milli_time()
                    out = self.outputbuffer.popleft()
                    try:
                        self.socket.send(out)
                    except OSError:
                        if self.socket.fileno() < 0:
                            return
                        raise Server.ServerConnectionException(self)

    def write_raw(self, binary):
        """Write binary to the output buffer."""
        self.outputbuffer.append(binary)
        self.log('Out', binary.decode())

    def write_cmd(self, command, text):
        """Write <command> with <text> to the output buffer."""
        message = command + ' ' + text
        self.write_raw(encode(message) + b"\n")

    def write_nocmd(self, text):
        """Write to the output buffer."""
        message = text
        self.write_raw(encode(message) + b"\n")

    def setuser(self):
        """Run the USER and NICK commands."""
        self.log('Init', 'USER and NICK: %s:%s' % (self.nick, self.name))
        self.write_cmd('USER', '%s 8 * :%s' % (self.nick, self.name))
        self.write_cmd('NICK', self.nick)

    def reconnect(self):
        """Reconnect to the server."""
        self.properties['joined'] = False
        self.socket.close()
        self.connect()

    def connect(self):
        """Connect to the server."""
        import pprint
        try:
            import ssl
        except ImportError as e:
            if 'ssl' in self.entry and self.entry['ssl']:
                raise e

        def handle(e):
            if 'ssl_force' not in self.entry or not self.entry[
                'ssl_force']:
                print(('Invalid Certificate. ' +
                'Add "ssl_force: True" to your ' +
                'server entry to force connection.'))
                pprint.pprint(self.socket.getpeercert())
                raise e
        try:
            self.state['lastpong'] = time.time()
            self.socket = socket.socket()
            if self.ssl:
                context = ssl.create_default_context()
                self.socket = context.wrap_socket(
                    self.socket, server_hostname=self.ssl)
            self.log('Init', 'Connecting to %s:%d%s' % (
                self.address, self.port, ' (SSL)' if self.ssl else ''))
            if self.ssl:
                try:
                    self.socket.connect((self.address, self.port))
                    ssl.match_hostname(self.socket.getpeercert(),
                        self.ssl)
                except ssl.CertificateError as e:
                    handle(e)
                except ssl.SSLError as e:
                    handle(e)
            else:
                self.socket.connect((self.address, self.port))
            self.setuser()
            self.log('Init', 'Connection succeded.')
        except OSError:
            raise Server.ServerConnectException(self)
        self.connecttimes = 0

    def socketready(self):
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
            if ircmsg and ircmsg[0] == ':':
                self.process_message(splitparse.SplitParser(ircmsg))

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
        """Process a SplitParser"""
        if sp.iscode('endmotd') and not self.properties['joined']:
            self.initjoin()
        self.do_base_hook('prerecv', fullparse.FullParse(self, sp))
        self.do_base_hook('recv', fullparse.FullParse(self, sp))

    def reiniting(self):
        """Called upon a reinit"""
        if self.socket:
            self.socket.send(b"QUIT :I'll be back soon!\n")
            self.socket.close()

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
