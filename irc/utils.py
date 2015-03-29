# -*- coding: utf-8 -*-


def stripuser(u):
    return u.strip('@+')


def ctcp(t):
    return '\1%s\1' % t