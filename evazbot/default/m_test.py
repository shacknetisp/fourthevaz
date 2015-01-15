# -*- coding: utf-8 -*-
from base import *


def get(ct):
    if(ct.cmd('test')):
        ct.msg('"%s"' % str(ct.args.getbool("test")))
        ct.msg('"%s"' % ct.args.get("test", "not"))
        ct.msg('"%s"' % ct.args.getdef())