# -*- coding: utf-8 -*-
from . import safeeval
import importlib
import utils
importlib.reload(safeeval)
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
                    'name': 'truth',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Output as a truth value.',
                    },
                {
                    'name': 'expr',
                    'optional': False,
                    'end': True,
                    'help': 'The expression to evaluate.',
                    },
                ],
            })
    #Math
    m.add_short_command_hook(
        lt,
        'lt::Return if <a> < <b>.',
        ['a::Value to test.',
        'b::Value to test.'])
    m.add_short_command_hook(
        gt,
        'gt::Return if <a> > <b>.',
        ['a::Value to test.',
        'b::Value to test.'])
    m.add_short_command_hook(
        eq,
        'eq::Return if <a> == <b>.',
        ['a::Value to test.',
        'b::Value to test.'])
    return m


def lt(fp, args):
    try:
        return str(float(args.getlinstr('a')) < float(args.getlinstr('b')))
    except ValueError:
        return 'Not numbers!'


def gt(fp, args):
    try:
        return str(float(args.getlinstr('a')) > float(args.getlinstr('b')))
    except ValueError:
        return 'Not numbers!'


def eq(fp, args):
    try:
        return str(float(args.getlinstr('a')) == float(args.getlinstr('b')))
    except ValueError:
        try:
            return str(utils.boolstr(args.getlinstr('a')) ==
            utils.boolstr(args.getlinstr('b')))
        except ValueError:
            return 'Not numbers!'


def calc(fp, args):
    arg = args.getlinstr('expr')
    try:
        if 'truth' in args.lin:
            return str(bool(round(safeeval.domath(arg))))
        return('%s' % (str(float(safeeval.domath(arg)))))
    except Exception as e:
        return('Error: ' + str(e))
