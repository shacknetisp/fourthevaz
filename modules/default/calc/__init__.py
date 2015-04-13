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
        'flipcoin':
            ' '.join("""
            if <calc -truth randrange(0, 2)>
            "echo <*if <eq <if <gt <wc $*> 0> 'echo $*' 'echo 0'> 1>
                'echo True' 'echo Heads'>"
            "echo <*if <eq <if <gt <wc $*> 0> 'echo $*' 'echo 0'> 1>
                'echo False' 'echo Tails'>"
            """.split()),
        })
    m.add_short_command_hook(dice,
        'dice::Roll dice.',
        ['[form]::Form of the dice, [<number>]d<sides>'])
    return m


def dice(fp, args):
    import random
    default = '1d6'
    invalidformat = 'Invalid format. Use [<number>]d<sides>.'
    try:
        try:
            number = int(args.getlinstr('form', default).split('d')[0])
            sides = int(args.getlinstr('form', default).split('d')[1])
        except ValueError:
            number = int(default.split('d')[0])
            sides = int(args.getlinstr('form', default).split('d')[1])
    except IndexError:
        return invalidformat
    except ValueError:
        return invalidformat
    if number < 1 or sides < 1:
        return "You won't get very many results with those numbers."
    if number > 450 / len(str(sides)):
        return "I don't want to roll that many dice."
    output = []
    for i in range(number):
        n = random.randrange(0, sides) + 1
        s = str(n)
        output.append(s)
    final = [utils.ltos(output, ', ')]
    return (" -- ".join(final))


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
            return args.getlinstr('a') == args.getlinstr('b')


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
