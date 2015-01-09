'''
#Copy the contents of this comment
#Add somthing like this to profiles.py in your ~/.fourthevaz folder
#Fourth Evaz should only connect to one IRC network
#(freenode, slashnet, etc...) at a time, but can have multiple connections.
#Note that you *can* have several networks, but it might mess up the
#whitelist and adminlist authentication systems.
ircprofiles = [
    {
        "ircsock": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        "server": "irc.freenode.net",
        "channels": ["#channel1", "#channel2"],
        "nick": "fourthevaz",
        "name": "Fourth Evaz",
        "whitelist": "freenode"
    },
    {
        "ircsock": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        "server": "irc.freenode.net",
        "channels": ["#channel3"],
        "nick": "Ivanbot",
        "name": "Ivan",
        "whitelist": "freenode",
    },
]
password="mypasswordforircauth"
moduleset="default" #change the moduleset
'''
#Don't copy these lines at all:
import evazbot.configs.c_locs as c_locs
moduleset = "default"
exec(open(c_locs.dbhome + "/profiles.py").read())