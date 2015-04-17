# -*- coding: utf-8 -*-
import configs.module
import urllib
import shlex
import utils


def init():
    m = configs.module.Module('reusage')
    m.set_help('Work with the Red Eclipse usage.cfg file.')
    m.add_short_command_hook(reusage,
        'reusage::Read the latest Red Eclipse usage.cfg',
        ['[-find]::Search for a command.',
            'name...::Name to look up or search query.'])
    return m


def reusage(fp, args):
    parsed = {}
    args.getlinstr('name')
    for line in urllib.request.urlopen(
        ('https://raw.githubusercontent.com/' +
        'red-eclipse/base/master/config/usage.cfg')
        ).read().decode().split('\n'):
        line = line.replace('(concatword $w ', 'weapon')
        line = line.replace(' $m)', '#')
        line = line.replace(') ', ' ')
        lex = shlex.shlex(line, posix=True)
        lex.commenters = ''
        lex.wordchars += '#'
        lex.whitespace_split = True
        lex.escape = '^'
        split = list(lex)
        if len(split) == 4:
            if split[0] == 'setdesc':
                parsed[split[1]] = "%s {%s}" % (
                    split[2],
                    split[3]
                    )
    found = []
    for command in parsed:
        if 'find' in args.lin:
            if configs.match.matchnocase(command, args.getlinstr('name'),
                False):
                found.append(command)
            elif configs.match.matchnocase(parsed[command],
                args.getlinstr('name'), False):
                found.append(command)
        else:
            if command.strip('#') == args.getlinstr('name').strip('#'):
                found.append('%s: %s' % (command, parsed[command]))
                break
    if found:
        return utils.ltos(sorted(found))
    else:
        return 'Nothing found.'