#Add something like this to profiles.py in your ~/.fourthevaz folder
#profiles definition
ircprofiles = [
    #one profile
    {
        #the socket, no need to change this (usually)
        "ircsock": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        #the IRC server
        "server": "irc.freenode.net",
        #the channels to join
        "channels": ["#channel1", "#channel2"],
        #the nick to use
        "nick": "fourthevaz",
        #the real name to use
        "name": "Fourth Evaz",
        #the whitelist section to use, see wlist.py
        "whitelist": "freenode",
	#optional command prefix, defaults to '.'
	"prefix": "~",
    },
    #another profile
    {
        "ircsock": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        "server": "irc.freenode.net",
        "channels": ["#channel3"],
        "nick": "Ivanbot",
        "name": "Ivan",
        "whitelist": "freenode",
    },
]
#the password used to auth nicks, see coremodules/m_auth.py
password = "mypasswordforircauth"
#change the moduleset
moduleset = "default"
