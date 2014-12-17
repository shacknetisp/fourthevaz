# -*- coding: utf-8 -*-
#This will import all essential Fourth Evaz components
from base import *


#The message-received event
def msg(mp):
    #if .example is received as a command
    if mp.cmd("example"):
        #Send a message echoing the arguments.
        main.sendcmsg("Example's Arguments: " + mp.args())
        #Command was received
        return True
    #No command received
    return False


#The ".help example" event
def showhelp():
    #Send a basic help message
    main.sendcmsg(".example <arguments>: Return the arguments.")