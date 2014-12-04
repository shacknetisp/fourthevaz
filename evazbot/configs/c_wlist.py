# -*- coding: utf-8 -*-
from imp import reload


def ghostsmember(n, i, ia, r=False, ac = 1):
    global whitelist
    global adminlist
    global names
    if r:
        fn = "[*Ghosts*] " + n
    else:
        fn = "[Ghosts] " + n
    whitelist.append((ac, (fn, i)))
    names.append(([fn, i], ia))
    
def ghostsmemberp(n, i, ia, r=False, ac = 1):
    global whitelist
    global adminlist
    global names
    if r:
        fn = "(*ghosts*)" + n
    else:
        fn = "(ghosts)" + n
    whitelist.append((ac, (fn, i)))
    names.append(([fn, i], ia))


whitelist = [
    # In Game,#IRC,
    (99, ("Alliance | sharidan2214", "sharidan2214")),
    (99, ("Iceflower", "Iceflower")),
    (99, ("", "Miner_48er")),
    (1,  ("Alliance | boozo", "Alliance || boozo", "bamboozle")),
    (99, ("Duckdef","DuckDef","*ACE* Dorment mammu","*ACE* Tristan","*ACE* Levi")),
    (99, ("SamsaraS.G.>DOOM<","")),
]

adminlist = [
    (1000, ":behalebabo!~snisp@cpe-67-251-6-219.maine.res.rr.com"),
    (999, ":Piggybear87!~Piggybear@96.58.129.198"),
    (99, ":sharidan2214!69e0a3c7@gateway/web/freenode/ip.105.224.163.199"),
    (99, ":Duckdef!~Umma@2601:b:9a00:283:b56d:48b4:1423:e56"),
]

names = [
    (["sharidan2214","Alliance | sharidan2214"], "Sharidan"),
    (["SamsaraS.G.>DOOM<","SniperGoth"], "Sniper.Goth"),
    (["Duckdef","*ACE* Levi"], "Levi"),
]

ghostsmember("Beha", "behalebabo", "Beha", False, 999)
ghostsmember("Piggybear", "Piggybear87", "[P]iggybear", False, 999)
ghostsmember("JFault", "acz13", "Jfault", False, 99)
ghostsmemberp("Galgul", "[~][~][~]", "Galgul", True, 99)
ghostsmember("Capitro", "jd3466", "Capitro", False)

