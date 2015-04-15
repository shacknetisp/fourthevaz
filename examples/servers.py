#The file itself is a list parsed by ast
[
  #Each server is a dictionary
  {
    #The settings key is the name of the database to use.
    #The database stores aliases and module settings.
    #You can use one database in several servers.
    'settings': 'freenode',
    #This is the server to connect to
    'address': {'host': 'irc.freenode.net', 'port': 6697},
    #The nick and name are defined here
    'id': {'nick': 'mybotsnick', 'name': 'An Example Bot'},
    #SSL Connection
    ##The address to check the certificate.
    ##Leave 'ssl' blank or do not include it to disable SSL.
    'ssl': 'irc.freenode.net',
    ##Force an ssl connect even if the hostnames do not match.
    ##Do not include this for the default of False.
    'ssl_force': False,
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