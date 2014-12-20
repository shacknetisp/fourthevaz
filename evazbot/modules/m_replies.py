# -*- coding: utf-8 -*-

from base import *
import evazbot.configs.wordai as wordai
reload(wordai)
cdb = wordai.wordai(c_locs.dbhome + '/replies.db.pkl')
cgdb = wordai.wordai(c_locs.dbhome + '/replies.cg.db.pkl')


def getmessage(msg, iss):
    fcstring_i = " :"
    fcstring_g = "> "
    if msg.find(fcstring_i) != -1 and not iss:
        loc = msg.find(fcstring_i) + len(fcstring_i) + 1
        args = msg[loc:]
    elif msg.find(fcstring_g) != -1:
        loc = msg.find(fcstring_g) + len(fcstring_g) + 1
        args = msg[loc:]
    else:
        args = ""
    return args


def msg(mp):
    if mp.wcmd('c'):
        cdb.load()
        if mp.argbool('fix'):
            if not mp.argbool('w') or not mp.argbool('n'):
                main.sendcmsg('Invalid Arguments')
                return True
            w = mp.argstr('w').strip()
            n = mp.argstr('n').strip()
            try:
                cdb.replace(w, n)
                main.sendcmsg("Replaced '" + w + "' with '" + n + "'")
            except KeyError:
                main.sendcmsg("'" + w + "' is not in the database.")
            return True
        elif mp.argbool('words'):
            main.sendcmsg('Words: ' + str(cdb.getwords()))
        else:
            main.sendcmsg(cdb.process(mp.args()))
    elif mp.cmd('cg'):
        cgdb.load()
        if mp.argbool('fix'):
            if not mp.argbool('w') or not mp.argbool('n'):
                main.sendcmsg('Invalid Arguments')
                return True
            w = mp.argstr('w').strip()
            n = mp.argstr('n').strip()
            try:
                cgdb.replace(w, n)
                main.sendcmsg("Replaced '" + w + "' with '" + n + "'")
            except KeyError:
                main.sendcmsg("'" + w + "' is not in the database.")
            return True
        elif mp.argbool('words'):
            main.sendcmsg('Words: ' + str(cgdb.getwords()))
        else:
            main.sendcmsg(cgdb.process(mp.args()))
    elif main.ircprofiles[main.currentprofile]["joined"] and\
    mp.ircuser() != "no_name":
        cgdb.load()
        cgdb.process(getmessage(mp.text(), mp.isserver()))
    return False


def showhelp():
    main.sendcmsg('.c <text>: Process <text>.')
    main.sendcmsg('.c -words: See word count.')
    main.sendcmsg('.c -fix -w=<word> -n=<newword>: Rename a word.')
    main.sendcmsg('.cg instead of .c will use the all-text system.')
