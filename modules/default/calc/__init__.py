# -*- coding: utf-8 -*-
from . import safeeval
import importlib
importlib.reload(safeeval)
# -*- coding: utf-8 -*-
from configs.module import Module


def init():
    m = Module('calc')
    m.set_help('Calculate Mathematical Expressions.')
    m.add_command_hook('calc',
        {
            'function': calc,
            'help': 'Calculate an expression (Python Syntax).',
            'args': [
                {
                    'name': 'expr',
                    'optional': False,
                    'end': True,
                    'help': 'The expression to evaluate.',
                    },
                ],
            })
    return m


def calc(fp, args):
    arg = args.getlinstr('expr')
    try:
        fp.reply('(%s) = (%s)' % (
        arg, str(float(safeeval.domath(arg)))))
    except Exception as e:
        fp.reply('Error: ' + str(e))
