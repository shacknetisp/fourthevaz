# -*- coding: utf-8 -*-

from base import *
import subprocess
reload(subprocess)
import evazbot.configs.wordai as wordai
reload(wordai)
wordai.dbfile = c_locs.dbhome + '/replies.db.pkl'
wordai.load()


def msg(mp):
    if mp.wcmd('c'):
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
    return False


def showhelp():
    main.sendcmsg('.c <text>: Process <text>.')
    main.sendcmsg('.c -words: See word count.')
    main.sendcmsg('.c -fix -w=<word> -n=<newword>: Rename a word.')
