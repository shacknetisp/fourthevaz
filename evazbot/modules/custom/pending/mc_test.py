from base import *


def msg(mp):
  if(mp.cmd("test")):
    main.sendcmsg("Test!")
    
def showhelp():
  main.sendcmsg(".test: Run test stuff.")
