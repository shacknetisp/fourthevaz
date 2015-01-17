# -*- coding: utf-8 -*-
from base import *
l_quotes = mload("l_quotes")

dbfile = c_locs.dbhome + "/l_quotes.db.pkl"


def start():
    return ["tip"]


def get(ct):
    if ct.cmd("tip"):
        db = c_vars.variablestore(dbfile)
        try:
            db.load()
        except IOError:
            pass
        qdb = l_quotes.quotedb(db, 'tips', 'tip', 'tips', ct)
        if ct.args.getbool('add'):
            qdb.add(ct.args.getdef())
        elif ct.args.getbool('remove'):
            qdb.remove(ct.args.getdef())
        else:
            out = qdb.get(ct.args.getdef())
            if out is not None:
                ct.msg(out)
        return True
    return False


def showhelp(h):
    h("tip [<search>]: Get a random tip")
    h("tip -add <new tip>")
    h("tip -remove [<search>]: Delete a tip, uses Python RegEx")
