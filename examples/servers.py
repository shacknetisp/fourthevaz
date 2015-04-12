#The file itself is a list parsed by ast
[
  #Each server is a dictionary
  {
    #The settings key is the name of the database to use.
    #The database stores aliases and module settings.
    #You can use one database in several servers.
    'settings': 'freenode',
    #This is the server to connect to
    'address': {'host': 'irc.freenode.net', 'port': 6667},
    #The nick and name are defined here
    'id': {'nick': 'mybotsnick', 'name': 'An Example Bot'},
    #The modulesets to use, core is always included
    'modulesets': ['default'],
    #The nickserv password, accessable with %pass% in the nickserv module
    'nspassword': 'anickservpass',
    #The default prefixes for commands, each channel can define it's own
    'prefix': '. ! !! ~',
    #The channels to connect to
    'channels': [
        #A single string will use the server prefixes.
        '#channel1',
        #You can specify prefixes and the channel name in dictionary format.
        {'channel': '#channel2', 'prefix': '!'}
    ],
  },
]