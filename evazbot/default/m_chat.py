# -*- coding: utf-8 -*-

from base import *


def msg(mp):
    if mp.cmd('chat'):
        args = mp.args()
        splitargs = args.split()
        #name = mp.user()
        if len(splitargs) > 1:
            main.sendsmsg(splitargs[0], 'From ' + mp.userf() + '@'
                          + main.getchannel() + ': '
                          + args[len(splitargs[0]) + 1:])
        else:
            main.sendcmsg('Invalid Arguments!')
        return True
    if mp.acmd('say'):
        args = mp.args()
        splitargs = args.split()
        if mp.text().find('PRIVMSG '
                          + main.ircprofiles[main.currentprofile]['nick'
                          ]) != -1:
            if len(splitargs) > 1:
                main.sendsmsg(splitargs[0], args[len(splitargs[0])
                              + 1:])
            else:
                main.sendcmsg('Invalid Arguments!')
        else:
            main.sendcmsg('Run from within a query.')
        return True

    if mp.acmd('chathelp'):
        main.sendmsg(mp.user(), cmd.cprefix + 'say <channel> <message>')
        return True
    return False


def showhelp():
    time.sleep(0.25)
    main.sendcmsg(cmd.cprefix + "chat <channel> <message>: " +
     "Send <message> to <channel>. <channel> can be 'all'."
                  )
    main.sendcmsg(cmd.cprefix + "chathelp: Admin's guide for this module.")
