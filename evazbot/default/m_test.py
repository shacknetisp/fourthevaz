# -*- coding: utf-8 -*-
from base import *


def get(ct):
    if(ct.cmd('test')):
        ct.msg('test recieved')