# -*- coding: utf-8 -*-
from configs.module import Module
import random


def init():
    m = Module(__name__)
    m.set_help('"Spurious use of IRC leads to more spuriousness."')
    m.add_base_hook('recv', recv)
    m.add_base_hook('commands.ignore', commands_ignore)
    return m


def generateface():
    ears = (
        "([`",
        ")]'",
        )
    eyes = "oO0*-+"
    mouth = '_.,'
    eari = random.randrange(len(ears[0]))
    return "%s%s%s%s%s" % (ears[0][eari], random.choice(eyes),
        random.choice(mouth), random.choice(eyes), ears[1][eari])


def commands_ignore(fp, o):
    if fp.sp.text.count(
            '.') == len(fp.sp.text):
                o['ignore'] = True


def recv(fp):
    if fp.sp.iscode('privmsg'):
        if fp.sp.text.count(
            '.') == len(fp.sp.text):
                possible = [generateface()]
                possible += chr(random.choice(list(range(0x1F600, 0x1F640))))
                possible += chr(random.choice(list(range(0x2600, 0x26C3))))
                possible += chr(random.choice(list(range(0x2701, 0x27BF))))
                fp.reply(random.choice(possible))
