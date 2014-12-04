# -*- coding: utf-8 -*-
exec(open("base.py").read())
modname = "IRC Ping"


def ping():
    main.ircwrite("PONG :pingis")
    print("Ping Processed.")