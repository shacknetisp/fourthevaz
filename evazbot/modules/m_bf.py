# -*- coding: utf-8 -*-
from base import *
bfbackend = cload("bfbackend")
intext = ""


def msg(mp):
    global intext
    if mp.cmd('bf'):
        cmdinput = mp.args()
        cmdoutput = bfbackend.evaluate(cmdinput, intext)
        main.sendcmsg(cmdoutput)
        intext = ""
    if mp.cmd("bfinput"):
        intext = mp.args()
        main.sendcmsg("Input set to: " + intext)


def showhelp():
    main.sendcmsg(
        ".bf <code>: Run Brainf**k code according to stdin of .bfinput")
    main.sendcmsg(".bfinput <input>: Set .bf input for the next .bf call.")
