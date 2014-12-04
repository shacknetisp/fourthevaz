'''
#Add somthing like this to profiles.py in your ~/.fourthevaz folder
ircprofiles = [
    {
        "ircsock": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        "server": "irc.freenode.net",
        "channels": ["#channel1", "#channel2"],
        "nick": "fourthevaz",
        "name": "Fourth Evaz",
    },
    {
        "ircsock": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        "server": "irc.freenode.net",
        "channels": ["#channel3"],
        "nick": "Ivanbot",
        "name": "Ivan",
    },
]
'''
exec(open(c_locs.dbhome+"/profiles.py").read())