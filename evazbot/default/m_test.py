# -*- coding: utf-8 -*-
from base import *


def msg(mp, ct):
    if(ct.cmd('test')):
        ct.msg('test recieved')