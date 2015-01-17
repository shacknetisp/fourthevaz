# -*- coding: utf-8 -*-
from base import *
l_quotes = mload("l_quotes")

dbfile = c_locs.dbhome + "/l_quotes.db.pkl"


def start():
    return ["history"]


def get(ct):
    if ct.cmd("history"):
        db = c_vars.variablestore(dbfile)
        try:
            db.load()
        except IOError:
            pass
        qdb = l_quotes.quotedb(
            db, 'hists', 'history slice', 'history slices', ct)
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
    h("history [<search>]: Get a random history slice")
    h("history -add <new history slice>")
    h("history -remove [<search>]: Delete a history slice, uses Python RegEx")
