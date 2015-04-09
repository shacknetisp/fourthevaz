# -*- coding: utf-8 -*-


def stripuser(u):
    return u.strip('@+')


def ctcp(t):
    return '\1%s\1' % t


#Everything but italic was found here:
#http://stackoverflow.com/a/13382032
class formatcodes:

    reset = '\x0f'
    bold = '\x02'
    italic = '\x1d'
    reverse = '\x16'
    underline = '\x15'
    strike = '\x13'
    color = '\x03'

    white = 0
    black = 1
    darkblue = 2
    darkgreen = 3
    red = 4
    darkred = 5
    darkviolet = 6
    orange = 7
    yellow = 8
    lightgreen = 9
    cyan = 10
    lightcyan = 11
    blue = 12
    violet = 13
    darkgray = 14
    lightgray = 15

    def buildcolor(foreground=-1, background=-1):
        out = ""
        if foreground >= 0:
            out += formatcodes.color + '%d' % foreground
        if background >= 0:
            out += ',%d' % background
        return out