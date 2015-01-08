# -*- coding: utf-8 -*-
from base import *
import random

dbfile = c_redeclipse.dbhome + "/quotes.db.txt"


def msg(mp):
    if mp.wcmd("addquote"):
        args = mp.args("addquote")
        with open(dbfile, "a") as myfile:
            if args[0] == '<':
                myfile.write(args + "\n")
                main.sendcmsg("Quote added: " + args)
            else:
                myfile.write("<anonymous> " + args + "\n")
                main.sendcmsg("Quote added, anonymously: " + args)
        return True
    if mp.cmd("quote"):
        args = mp.args("quote")
        lines = []
        for line in open(dbfile, 'r'):
            if line.upper().find("<" + args.upper()) == 0:
                lines.append(line.strip())
        out = random.choice(lines)
        outfull = str.format('Quote: "{0}"', out)
        main.sendcmsg(outfull)
        return True
    if mp.wcmd("sortquotes"):
        lines = []
        for line in open(dbfile, 'r'):
            lines.append(line)
        lines.sort()
        with open(dbfile, 'w') as f:
            f.writelines(lines)
        main.sendcmsg("The quotes have been sorted.")
        return True
    return False


def showhelp():
    main.sendcmsg(
        ".quote <[start]>: Recall a random quote, match the beginning with " +
        "'<start' (literal '<' and 'start' represents the search pattern).")
    main.sendcmsg(".addquote <the quote>: Add <the quote>.")
    main.sendcmsg(".sortquotes: Clean the quote DB.")
