from base import *


def afterall(mp):
    if not main.handled:
        if mp.text().find("PRIVMSG "+main.getchannel()+" :.") != -1 or mp.text().find(mp.user()+"> .") != -1:
            main.sendcmsg("Unrecognized Command!")
            for i in c_modules.helpmodulenames():
               if mp.text().find("." + i) != -1:
                  main.sendcmsg("If you meant to call module "+i+", use: .help " + i);