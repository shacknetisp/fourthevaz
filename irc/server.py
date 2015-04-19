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
import os
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
        'tick_min': 200,
        'whois_tick_min': 1000,
        'recv_size': pow(2, 12),
        }):
        if entry['settings'] not in running.serverdb.db():
            running.serverdb.db()[entry['settings']] = {}
        self.db = running.serverdb.db()[entry['settings']]
        """Persistant dictionary for database-specific data."""
        if entry['settings'] not in running.accesslist.db():
            running.serverdb.accesslist()[entry['settings']] = {}
        self.adb = running.accesslist.db()[entry['settings']]
        """This server's access list."""
        self.state = {}
        """Temporary dictionary for server-specific data."""
        self.options = options
        self.address = address
        """IRC Server IP/Host"""
        self.port = port
        """IRC Server Port"""
        self.nick = nick
        """IRC Nick"""
        self.name = name
        self.outputbuffer = deque()
        self.logbuffer = []
        self.lasttick = 0
        self.lastwhoistick = 0
        self.socket = None
        self.ssl = ''
        if 'ssl' in entry:
            self.ssl = entry['ssl']
        self.entry = entry
        """Server's entry in servers.py"""
        self.channels = []
        """Current channels."""
        for c in channels:
            c = self.shortchannel(c)
            self.channels.append(c)
        self.properties = {}
        self.properties['joined'] = False
        self.modules = []
        self.reinit()
        self.reloaded = False
        self.whoisbuffer = []
        """List of nicks to run WHOIS on next."""
        self.whoislist = {}
        """WHOIS information list."""
        self.auth = entry['auth'] if 'auth' in entry else None
        """Tuple for auth: (<type>, [<account>] or "", <password>)."""

    def update_aliases(self):
        """Regenerate the alias database."""
        if 'aliases' not in self.db or type(self.db['aliases']) is not dict:
            self.db['aliases'] = {}
        d = {}
        try:
            d = ast.literal_eval(open(locs.userdata + '/aliases.py').read())
        except FileNotFoundError:
            pass
        self.aliasdb = utils.merge_dicts(d, self.db['aliases'])
        for m in self.modules:
            self.aliasdb = utils.merge_dicts(self.aliasdb, m.aliases)

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

    def reinit(self):
        """Completely reload the server's modules and aliases."""
        mload.serverinit(self)
        self.update_aliases()
        self.load_commands()

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

    def log(self, prefix, p_text):
        """Log <prefix>: <p_text>"""
        text = prefix + ': ' + p_text
        self.logbuffer.append(text)
        if self.options['print_log']:
            print((text.strip('\n')))

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

    def modulepaths(self):
        """Return a list of all paths where modules might be."""
        paths = [locs.cmoddir, 'modules/%s/' % "core"]
        for mset in self.entry['modulesets']:
            if os.path.isdir(locs.cmoddir + '/sets/%s' % mset):
                paths.append(locs.cmoddir + '/sets/%s' % mset)
            if os.path.isdir('modules/%s/' % mset):
                paths.append('modules/%s/' % mset)
        return paths

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
        if sp.iscode('endmotd') and not self.properties['joined']:
            self.initjoin()
        self.do_base_hook('prerecv', fullparse.FullParse(self, sp))
        self.do_base_hook('recv', fullparse.FullParse(self, sp))

    def do_base_hook(self, name, *args, **kwargs):
        """Do base hook <name> with <*args> and <**kwargs>."""
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
        """Unload module <name>."""
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

    def import_module(self, name, do_reload):
        """Return an imported module from the current modulesets."""
        return mload.import_module_py(
            name, self.entry['modulesets'], do_reload)

    def add_module(self, name, mset=[]):
        """Load module <name>."""
        if not mset:
            mset = self.entry['modulesets']
        self.delete_module(name)
        try:
            m = mload.import_module(
                name, mset, options={'server': self})
        except mload.DepException as e:
            print(('!!! -- Dependancy Exception in %s: %s' % (name, e.e)))
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