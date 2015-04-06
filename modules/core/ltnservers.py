# -*- coding: utf-8 -*-
import configs.module
import configs.mload
import utils


def init():
    m = configs.module.Module(__name__)
    m.set_help('Parse commands from servers.')
    m.add_command_hook('addserver', {
        'function': addserver,
        'help': 'Add a nick to the servers list.',
        'args': [
            {
                'name': 'nick',
                'optional': False,
                'help': 'Nick to add to the list'
                }
            ]
        })
    m.add_command_hook('removeserver', {
        'function': removeserver,
        'help': 'Removes a nick from the servers list.',
        'args': [
            {
                'name': 'nick',
                'optional': False,
                'help': 'Nick to remove from the list.'
                }
            ]
        })
    m.add_command_hook('listservers', {
        'function': listservers,
        'help': 'Show server list.',
        'args': []
        })
    m.add_base_hook('recv', recv)
    return m


def isredeclipse(fp):
    user = fp.sp.sendernick
    if user in fp.server.whoislist and 'done' in fp.server.whoislist[user]:
        return fp.server.whoislist['ident'] == '~redeclips'


def addserver(fp, args):
    if 'ltnservers' not in fp.server.db:
        fp.server.db['ltnservers'] = []
    fp.server.db['ltnservers'].append(args.getlinstr('nick'))
    return '%s is now in the server list.' % args.getlinstr('nick')


def removeserver(fp, args):
    try:
        del fp.server.db['ltnservers'][
            fp.server.db['ltnservers'].index(args.getlinstr('nick'))]
        return '%s has been removed from the server list.' % args.getlinstr(
            'nick')
    except KeyError:
        pass
    except ValueError:
        pass
    return '%s is not in the server list.' % args.getlinstr('nick')


def listservers(fp, args):
    if 'ltnservers' not in fp.server.db:
        fp.server.db['ltnservers'] = []
    return 'Servers: ' + utils.ltos(fp.server.db['ltnservers'])


def recv(fp):
    commands = configs.mload.import_module_py(
        'commands', fp.server.entry['moduleset'], False)
    if fp.ltnserver():
        if fp.sp.iscode('QUIT') or fp.sp.iscode('PART'):
            for k in fp.server.state:
                if k.find('%s.authname.' % fp.sp.sendernick) == 0:
                    fp.server.state[k] = ''
        ptext = ""
        fp.sp.text = fp.sp.text.replace('\x0f', '')
        try:
            fp.user = utils.find_between(fp.sp.text, '<', '> ')
        except IndexError:
            fp.user = ''
        fp.setaccess("%s==" % fp.user)
        if isredeclipse(fp):
            if (fp.sp.text.find('has joined the game') != -1 and
            fp.sp.text.count(')') == 3 and
            fp.sp.text.count('(') == 3 and
            fp.sp.text[-1] == ')'):
                fp.user = ' '.join(fp.sp.text.split(
                    'has joined the game')[
                    0].split()[:-1])
                fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    fp.user)] = fp.sp.text.split()[-4].strip(')')
                return
            if (fp.sp.text.find('has left the game') != -1 and
            fp.sp.text.count(')') == 2 and
            fp.sp.text.count('(') == 2 and
            fp.sp.text[-1] == ')'):
                fp.user = ' '.join(fp.sp.text.split(
                    'has left the game')[
                    0].split()[:-1])
                del fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    fp.user)]
                return
            if (fp.sp.text.find('is now known as') != -1):
                s = fp.sp.text.split('is now known as')
                fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    s[1][1:])] = fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    s[0][2:-1])]
                del fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    s[0][2:-1])]
                return
            if (fp.sp.text.find('identified as') != -1):
                s = fp.sp.text.split('identified as')
                fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    s[0][:-1])] = s[1][1:].split()[-3]
                return
            try:
                authname = fp.server.state['%s.authname.%s' % (
                    fp.sp.sendernick,
                    fp.user)]
                fp.setaccess("%s==%s" % (fp.user, authname))
            except KeyError:
                pass
        text = fp.sp.text[fp.sp.text.index('> ') + 2:]
        prefixt = fp.channel.entry['prefix'].split()
        possible = [
            fp.server.nick + ', ',
            fp.server.nick + ': ',
            ] + prefixt
        found = False
        prefix = prefixt[0]
        for p in possible:
            if text.find(p) == 0:
                found = True
                prefix = p
                break
        if not found:
            return
        ptext = text[len(prefix):]
        if ptext:
            fp.reply(commands.doptext(fp, ptext))