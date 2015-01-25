# -*- coding: utf-8 -*-
#This will import all essential Fourth Evaz components
from base import *


#start() returns a list of commands to register
#this speeds up the event loop greatly
def start():
    #we use the command 'example'
    return ["example"]

###########With mp##########
'''
The message-received event
def msg(mp):
    #if .example is received as a command
    if mp.cmd("example"):
        #Send a message echoing the arguments to the current channel/query.
        main.sendcmsg("Example's Default Arguments: " +
        '"' + mp.argsdef() + '"')
        #Send a message echoing -test
        if mp.argbool("test"):
            main.sendcmsg('"' + mp.argstr("test") + '"')
        #Command was received
        return True
    #No command received
    return False
'''
#########With ct##############
# the message-received event


def get(ct):
    #if .example is received as a command
    if ct.cmd('example'):
        #Send a message echoing the arguments to the current channel/query.
        ct.msg("Example's Default Arguments: " +
               '"' + ct.args.getdef() + '"')
        #send a message echoing -test
        if ct.args.getbool('test'):  # checks if -test was called
            ct.msg('"' + ct.args.get("test") + '"')
        #Command was received
        return True
    return False

#The ".help example" event
# NEW


def showhelp(h):
    #Send a basic help message
    h("example <arguments>: Return the arguments.")

'''OLD
def showhelp():
    main.sendcmsg(
        cmd.cprefix() + 'example <arguments>: Return the arguments.')'''
