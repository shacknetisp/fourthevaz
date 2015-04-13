# -*- coding: utf-8 -*-
from configs.module import Module
import random


def init():
    m = Module(__name__)
    m.set_help('Random humorous replies.')
    m.add_base_hook('recv', recv)
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


def recv(fp):
    if fp.sp.code('privmsg'):
        if fp.sp.text and fp.sp.sendernick and fp.sp.text.count(
            '.') == len(fp.sp.text):
                fp.reply(generateface())
