# -*- coding: utf-8 -*-

from base import *
import subprocess
reload(subprocess)
import evazbot.configs.wordai as wordai
reload(wordai)
import evazbot.configs.wordai as wordaicg
reload(wordaicg)

def getmessage(msg,iss):
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
        wordai.dbfile = c_locs.dbhome + '/replies.db.pkl'
        wordai.load()
        if mp.argbool('fix'):
            if not mp.argbool('w') or not mp.argbool('n'):
                main.sendcmsg('Invalid Arguments')
                return True
            w = mp.argstr('w').strip()
            n = mp.argstr('n').strip()
            try:
                wordai.replace(w, n)
                main.sendcmsg("Replaced '" + w + "' with '" + n + "'")
            except KeyError:
                main.sendcmsg("'" + w + "' is not in the database.")
            return True
        elif mp.argbool('words'):
            main.sendcmsg('Words: ' + str(wordai.getwords()))
        else:
            main.sendcmsg(wordai.process(mp.args()))
    elif mp.wcmd('cg'):
        wordaicg.dbfile = c_locs.dbhome + '/replies.cg.db.pkl'
        wordaicg.load()
        if mp.argbool('fix'):
            if not mp.argbool('w') or not mp.argbool('n'):
                main.sendcmsg('Invalid Arguments')
                return True
            w = mp.argstr('w').strip()
            n = mp.argstr('n').strip()
            try:
                wordaicg.replace(w, n)
                main.sendcmsg("Replaced '" + w + "' with '" + n + "'")
            except KeyError:
                main.sendcmsg("'" + w + "' is not in the database.")
            return True
        elif mp.argbool('words'):
            main.sendcmsg('Words: ' + str(wordaicg.getwords()))
        else:
            main.sendcmsg(wordaicg.process(mp.args()))
    wordaicg.dbfile = c_locs.dbhome + '/replies.cg.db.pkl'
    wordaicg.load()
    wordaicg.process(getmessage(mp.text(),mp.isserver()))
    return False


def showhelp():
    main.sendcmsg('.c <text>: Process <text>.')
    main.sendcmsg('.c -words: See word count.')
    main.sendcmsg('.c -fix -w=<word> -n=<newword>: Rename a word.')
    main.sendcmsg('.cg instead of .c will use the all-text system.')
