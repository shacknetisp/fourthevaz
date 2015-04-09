# -*- coding: utf-8 -*-
import configs.module
import utils
from . import commands


def init():
    m = configs.module.Module(__name__)
    m.set_help('Various string and parser functions.')
    #Strings
    m.add_short_command_hook(
        wordcount,
        'wordcount::Get a count of words.',
        ['words...::Words to count.'])
    m.add_command_alias('wc', 'wordcount')
    #Logic
    m.add_short_command_hook(
        if_f,
        'if::If <value> then <then> else <else>.',
        ['value::Value to test.',
        'then::Command to execute if value.',
        'else::Command to execute if not value.',
        ])
    m.add_short_command_hook(
        or_f,
        'or::Return if <a> or <b>',
        [
            'a::Value to test',
            'b::Value to test',
            ]
        )
    m.add_short_command_hook(
        and_f,
        'and::Return if <a> and <b>',
        [
            'a::Value to test',
            'b::Value to test',
            ]
        )
    m.add_short_command_hook(
        not_f,
        'not::Return not <a>',
        [
            'a::Value to reverse',
            ]
        )
    m.add_aliases({
        'nand': 'not <and $# $#>',
        'nor': 'not <or $# $#>',
        'xor': 'not <eq <not $#> <not $#>>'
        })
    return m


def not_f(fp, args):
    try:
        return str(not utils.boolstr(args.getlinstr('a')))
    except ValueError:
        return 'Invalid truth value.'


def or_f(fp, args):
    try:
        return str(utils.boolstr(args.getlinstr('a')) or utils.boolstr(
            args.getlinstr('b')))
    except ValueError:
        return 'Invalid truth value.'


def and_f(fp, args):
    try:
        return str(utils.boolstr(args.getlinstr('a')) and utils.boolstr(
            args.getlinstr('b')))
    except ValueError:
        return 'Invalid truth value.'


def wordcount(fp, args):
    return str(len(args.getlinstr('words', '').split()))


def if_f(fp, args):
    try:
        if utils.boolstr(args.getlinstr('value')):
            return commands.doptext(fp, args.getlinstr('then'))
        else:
            return commands.doptext(fp, args.getlinstr('else'))
    except ValueError:
        return 'Invalid truth value.'