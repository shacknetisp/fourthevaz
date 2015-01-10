# -*- coding: utf-8 -*-
from base import *
bfbackend = mload("m_bf.backend")
intext = ""


def msg(mp):
    global intext
    if mp.cmd('bf'):
        cmdinput = mp.args()
        cmdoutput = bfbackend.evaluate(cmdinput, intext)
        main.sendcmsg(
            cmdoutput[0:min(len(cmdoutput), 255)]
            .replace("\n", " ").replace("\r", " "))
        intext = ""
    if mp.cmd("bfinput"):
        intext = mp.args()
        main.sendcmsg("Input set to: " + intext)


def showhelp():
    main.sendcmsg(
        cmd.cprefix() +
        "bf <code>: Run Brainf**k code according to stdin of .bfinput")
    main.sendcmsg(cmd.cprefix() +
    "bfinput <input>: Set .bf input for the next .bf call.")
