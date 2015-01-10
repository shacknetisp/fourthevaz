# -*- coding: utf-8 -*-
#Add something like this to wlist.py in your ~/.fourthevaz folder
#basic whitelist

#profiles definition
profiles = {

    #a whitelist section, referenced from profiles.py
  'freenode': {

      #nicks and their access levels
      #you don't need to use this often because of .wlist
    'whitelist': [
      (99, ["behalebabo"]),
      ],

    #set noauth to true if the network doesn't support logging in
    #if noauth is true, the adminlist uses nick rather than login name
    'noauth': False,
    'adminlist': [
      (1000, "behalebabo"),
      ],

        #nicks and their assigned names
    'names': [
      (["behalebabo"], "Beha"),
      ]}
    }

