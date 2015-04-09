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
                    'name': '{truth/int}',
                    'optional': True,
                    'keyvalue': '',
                    'help': 'Output as a truth/rounded int value.',
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
    m.add_aliases({
        'random': 'calc uniform($1, $2)~~0~~100',
        'randint': 'calc randrange($1, $2)~~0~~100',
        'dice':
            'if <gt $1 0> ' +
                '"echo You roll <*calc -int <randint 0 $1> + 1> out of $1."' +
                ' "echo The die must have at least 1 side."~~6',
        'flipcoin':
            'if <calc -truth randrange(0, 2)> "echo heads" "echo tails"',
        })
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
        elif 'int' in args.lin:
            return str(int(round(safeeval.domath(arg))))
        return('%s' % (str(float(safeeval.domath(arg)))))
    except Exception as e:
        return('Error: ' + str(e))
