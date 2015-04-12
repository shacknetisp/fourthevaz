# -*- coding: utf-8 -*-
import configs.locs
import os
import db.text
import configs.mload
import random
import utils


class LineDB:

    def __init__(self, name, plural, seperprefix,
        seper, add, main, remove, showlist, random, eh=''):
        self.dbfolder = configs.locs.userdb + '/' + plural
        os.makedirs(self.dbfolder, exist_ok=True)
        self.name = name
        self.plural = plural
        self.seperprefix = seperprefix
        self.seper = seper
        self.f_add = add
        self.f_main = main
        self.f_remove = remove
        self.f_list = showlist
        self.random = random
        self.randomtext = "random" if random else "single"
        self.eh = eh

    def splitline(self, i1, i2=""):
        r1 = i2
        r2 = i1
        if i1 and i1[0].find(self.seperprefix) == 0:
            r1 = i1.split()[0]
            r2 = ' '.join(i1.split()[1:])
        return (r1, r2)

    def initserver(self, server):
        path = "%s/%s.py" % (
            self.dbfolder, server.entry['settings'])
        server.state['%s.db' % self.plural] = db.text.DB(path)
        if os.path.exists(path):
            server.state['%s.db' % self.plural].load()
        server.state['%s.db' % self.plural].save()

    def configure(self, m):
        m.set_help('Store and retrieve %s.' % self.plural)
        m.add_command_hook('add',
            {
                'rights': ['normal'],
                'function': self.f_add,
                'help': 'Add a %s to the database.' % self.name,
                'args': [
                    {
                    'name': '%s' % self.name,
                    'optional': False,
                    'help': str(
                        'The %s, in this format: [%s%s] <%s>.%s,' % (
                        self.name, self.seperprefix, self.seper, self.name,
                        self.eh)),
                    'end': True,
                    }
                    ]
                })
        m.add_command_hook('%stopics' % self.name,
            {
                'function': self.f_list,
                'help': 'View %s topics.' % self.name,
                'args': []
                })
        m.add_command_hook(self.name,
            {
                'function': self.f_main,
                'noquote': True,
                'help': 'Get a %s %s.' % (self.randomtext, self.name),
                'args': [
                    {
                    'name': 'add',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Alias for %s.add.' % m.name,
                    },
                        {
                    'name': 'remove',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Alias for %s.remove.' % m.name,
                    },
                        {
                    'name': 'force',
                    'optional': True,
                    'keyvalue': '',
                    'help': '-force option for remove alias.',
                    },
                    {
                    'name': self.name,
                    'optional': True,
                    'help': str(
                        'The %s, in this format: [%s%s] <search>.%s' % (
                        self.name, self.seperprefix, self.seper, self.eh)),
                    'end': True,
                    }
                    ]
                })
        m.add_command_hook('remove',
            {
                'function': self.f_remove,
                'help': 'Remove a %s.' % self.name,
                'rights': ['normal'],
                'args': [
                        {
                    'name': 'force',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Force removal of multiple quotes.',
                    },
                    {
                    'name': self.name,
                    'optional': True,
                    'help': str(
                        'The %s, in this format: [%s%s] <search>.' % (
                        self.name, self.seperprefix, self.seper)),
                    'end': True,
                    }
                    ]
                })

    def add(self, fp, args, dt, channel=False):
        line = args.getlinstr(self.name)
        topic, line = self.splitline(line,
            dt)
        if topic == "":
            return 'You must specify a topic.'
        if channel and fp.channelaccess(topic) < 1:
                return 'You must be at least level 1 in the target channel.'
        if (topic not in fp.server.state['%s.db' % self.plural].db()) or (
            not self.random):
            fp.server.state['%s.db' % self.plural].db()[topic] = []
        if line in fp.server.state['%s.db' % self.plural].db()[topic]:
            return 'That line already exists.'
        fp.server.state['%s.db' % self.plural].db()[topic].append(line)
        fp.server.state['%s.db' % self.plural].save()
        return '"%s" has been added to %s %s' % (line, self.seper, topic)

    def main(self, fp, args, dt):
        commands = fp.server.import_module('commands', False)
        line = args.getlinstr(self.name, '')
        if 'add' in args.lin:
            return commands.doptext(fp, '%s.add %s' % (self.plural, line))
        elif 'remove' in args.lin:
            return commands.doptext(fp, '%s.remove %s%s' % (self.plural,
                "-force " if 'force' in args.lin else '',
                line))
        topic, line = self.splitline(line,
           dt)
        db = fp.server.state['%s.db' % self.plural].db()
        if topic not in db or len(db[topic]) == 0:
            if not topic:
                return 'No lines found.'
            return 'There are no lines for %s' % topic
        choices = []
        for q in db[topic]:
            if configs.match.matchnocase(q, line, False):
                choices.append(q)
        if not choices:
            return 'No matching lines found.'
        return random.choice(choices)

    def showlist(self, fp, args):
        return 'Topics: ' + utils.ltos(
            fp.server.state['%s.db' % self.plural].db())

    def remove(self, fp, args, dt, channel=False):
        line = args.getlinstr(self.name, '')
        topic, line = self.splitline(line,
            dt)

        if channel and fp.channelaccess(topic) < 1:
                return 'You must be at least level 1 in the target channel.'

        db = fp.server.state['%s.db' % self.plural].db()
        if topic not in db or len(db[topic]) == 0:
            if not topic:
                return 'No lines found.'
            return 'There are no lines for %s' % topic
        choices = []
        for qi in range(len(db[topic])):
            q = db[topic][qi]
            if configs.match.matchnocase(q, line, False):
                choices.append(qi)
        if not choices:
            return 'No matching lines found.'
        if len(choices) > 1 and 'force' not in args.lin:
            return '%d lines selected, use -force to delete.' % len(choices)
        todelete = db[topic][choices[0]]
        db[topic] = utils.remove_indices(db[topic], choices)
        fp.server.state['%s.db' % self.plural].save()
        if len(choices) > 1:
            return 'Deleted %d lines.' % len(choices)
        else:
            return 'Deleted "%s".' % todelete

