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
        ptext = ""
        try:
            fp.user = utils.find_between(fp.sp.text, '<', '> ')
            fp.setaccess("%s::" % fp.user.replace(':', '"'))
            text = fp.sp.text[fp.sp.text.index('> ') + 2:]
            prefix = fp.channel.entry['prefix']
            possible = [
                prefix,
                fp.server.nick + ', ',
                fp.server.nick + ': ',
                ]
            found = False
            for p in possible:
                if text.find(p) == 0:
                    found = True
                    prefix = p
                    break
            if not found:
                return
            ptext = text[len(prefix):]
        except IndexError:
            pass
        except ValueError:
            pass
        if ptext:
            fp.reply(commands.doptext(fp, ptext))