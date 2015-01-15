# -*- coding: utf-8 -*-
from base import *
l_quotes = mload("l_quotes")

dbfile = c_locs.dbhome + "/l_quotes.db.pkl"


def get(ct):
    if ct.cmd("joke"):
        db = c_vars.variablestore(dbfile)
        try:
            db.load()
        except IOError:
            pass
        qdb = l_quotes.quotedb(db, 'jokes', 'joke', 'jokes', ct)
        if ct.args.getbool('add'):
            qdb.add(ct.args.getdef())
        elif ct.args.getbool('remove'):
            qdb.remove(ct.args.getdef())
        else:
            if ct.args.getbool('target'):
                out = qdb.get(ct.args.getdef(), '#target')
            else:
                out = qdb.get(ct.args.getdef(), '', '#target#')
            if out is not None:
                ct.msg(out.replace('#target#', ct.args.get(
                    'target')).replace('#caller#', ct.user()))
        return True
    return False


def showhelp(h):
    h("joke [-target=<target>] [<search>]: Get a random joke")
    h("joke -add <new joke>: #target# and #caller# are the tokens.")
    h("joke -remove [<search>]: Delete a joke, uses Python RegEx")