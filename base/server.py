# -*- coding: utf-8 -*-
import configs.mload as mload
import configs.locs as locs
import moduleregistry
import running
import utils
import string
import ast
import os
moduleregistry.add_module(mload)


class Server:

    def __init__(self, entry, options):
        if entry['settings'] not in running.serverdb.db():
            running.serverdb.db()[entry['settings']] = {}
        self.db = running.serverdb.db()[entry['settings']]
        """Persistant dictionary for database-specific data."""
        if entry['settings'] not in running.accesslist.db():
            running.accesslist.db()[entry['settings']] = {}
        self.adb = running.accesslist.db()[entry['settings']]
        """This server's access list."""
        self.state = {}
        """Temporary dictionary for server-specific data."""
        self.options = options
        self.logbuffer = []
        self.entry = entry
        """Server's entry in servers.py"""
        self.properties = {}
        self.modules = []
        self.reloaded = False

    def reiniting(self):
        pass

    def connect(self):
        pass

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

    def reinit(self):
        """Completely reload the server's modules and aliases."""
        mload.serverinit(self)
        self.update_aliases()
        self.load_commands()

    def log(self, prefix, p_text):
        """Log <prefix>: <p_text>"""
        text = prefix + ': ' + p_text
        text = ''.join([x for x in text if x in string.printable])
        self.logbuffer.append(text)
        if self.options['print_log']:
            print((text.strip('\n')))

    def modulepaths(self):
        """Return a list of all paths where modules might be."""
        core = 'modules/%s/' % "core"
        paths = [locs.cmoddir, core]

        def a(p):
            if os.path.isdir(p + '/%s' % self.type):
                paths.append(p + '/%s' % self.type)
        a(core)
        a(locs.cmoddir)
        for mset in self.entry['modulesets']:
            d = locs.cmoddir + '/sets/%s' % mset
            if os.path.isdir(d):
                paths.append(d)
                a(d)
            d = 'modules/%s/' % mset
            if os.path.isdir(d):
                paths.append(d)
                a(d)
        return paths

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