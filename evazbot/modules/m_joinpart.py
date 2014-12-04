# -*- coding: utf-8 -*-
exec(open("base.py").read())

def msg(mp):
    if(mp.isserver()):
      return
    if mp.isjp("JOIN"):
        main.sendamsg(cmd.getname(mp.ircuser()) + " is now in " + main.getchannel() + ".")
    elif mp.isjp("PART"):
        main.sendamsg(cmd.getname(mp.ircuser()) + " has departed " + main.getchannel() + ".")
    elif mp.isquit():
        main.sendamsg(cmd.getname(mp.ircuser()) + " has left IRC.")