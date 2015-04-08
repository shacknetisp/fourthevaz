# -*- coding: utf-8 -*-
from configs.module import Module
from irc.utils import formatcodes


def init():
    m = Module('echo')
    m.set_help('Echo text and provide various text functions.')
    m.add_command_hook('echo',
        {
            'function': echo,
            'help': 'Echo text.',
            'noquote': True,
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                ],
            })
    m.add_command_hook('absorb',
        {
            'function': absorb,
            'help': 'Absorb text.',
            'args': [
                {
                    'name': 'return',
                    'optional': False,
                    'help': 'Text to return.'
                    },
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                ],
            })
    m.add_command_hook('qecho',
        {
            'function': echo,
            'help': 'Echo text with quote.',
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                ],
            })
    m.add_command_hook('bold',
        {
            'function': bold,
            'help': 'Echo bold text.',
            'noquote': True,
            'args': [
                {
                    'name': 'text',
                    'optional': False,
                    'help': 'Text to echo.',
                    'end': True,
                    },
                ],
            })
    m.add_short_command_hook(italic,
        'italic::Echo italic text.',
        ['text...::Text to echo.'])
    m.add_short_command_hook(underline,
        'underline::Echo underlined text.',
        ['text...::Text to echo.'])
    m.add_short_command_hook(strike,
        'strike::Echo strikthroughed text.',
        ['text...::Text to echo.'])
    m.add_short_command_hook(color,
        'color::Echo colored text.',
        ['color::Color: fgnd,[bgnd].',
        'text...::Text to echo.'])
    return m


def echo(fp, args):
    return "%s" % (args.getlinstr('text', ''))


def absorb(fp, args):
    return "%s" % (args.getlinstr('return', ''))


def bold(fp, args):
    return formatcodes.bold + "%s%s" % (
        args.getlinstr('text', ''), formatcodes.reset
        if args.getlinstr('text', '') else '')


def italic(fp, args):
    return formatcodes.italic + "%s%s" % (
        args.getlinstr('text', ''), formatcodes.reset
        if args.getlinstr('text', '') else '')


def underline(fp, args):
    return formatcodes.underline + "%s%s" % (
        args.getlinstr('text', ''), formatcodes.reset
        if args.getlinstr('text', '') else '')


def strike(fp, args):
    return formatcodes.strike + "%s%s" % (
        args.getlinstr('text', ''), formatcodes.reset
        if args.getlinstr('text', '') else '')


def color(fp, args):
    return formatcodes.color + "%s%s%s" % (
        args.getlinstr('color'),
        args.getlinstr('text', ''), formatcodes.reset
        if args.getlinstr('text', '') else '')