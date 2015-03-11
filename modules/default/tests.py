# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('tests')
    m.set_help('Run tests.')
    m.add_command_hook('test',
        {
            'function': test,
            'help': 'Test fp.reply(), echo if specfied.',
            'args': [
                {
                    'name': 'echo2',
                    'keyvalue': 'text',
                    'optional': True,
                    'help': 'Echo this as an option.',
                    },
                        {
                    'name': 'echo3',
                    'optional': False,
                    'help': 'Echo this.',
                    },
                {
                    'name': 'echo',
                    'optional': True,
                    'help': 'Echo this.',
                    'end': True,
                    }
                ],
            })
    return m


def test(fp, args):
    fp.reply('%s,%s,%s' % (
        args.getlinstr('echo', ''),
        args.getlinstr('echo3', ''),
        args.getlinstr('echo2', '')))
