# -*- coding: utf-8 -*-

from base import *


def msg(mp):
    if mp.cmd('stats'):
        out = []
        custom_count = 0
        for i in c_modules.module_callbacks:
            if i[c_modules.custom_offset]:
                custom_count += 1
        tolist = mp.argbool('list')
        tomodules = mp.argbool('modules')
        tousers = mp.argbool('users')
        tochannels = mp.argbool('channels')
        nothing = not tomodules and not tousers and not tochannels
        if tomodules:
            m_totalstr = str(len(c_modules.module_callbacks))
            out.append(str(len(c_modules.modules)) + '/' + m_totalstr
                       + ' default/all modules.')
            out.append(str(custom_count) + '/' + m_totalstr
                       + ' custom/all modules.')
            out.append(str(len(c_modules.helpmodulenames()))
                       + ' interactive modules.')
            if tolist:
                names = []
                for i in c_modules.module_callbacks:
                    names.append(i[c_modules.name_offset])
                cmd.outlist(['Modules'] + names)
        if tousers:
            wlistnames = []
            for i in c_wlist.whitelist:
                    found = False
                    for n in i[1]:
                        if n and not found:
                            found = True
                            wlistnames.append(cmd.getname(n))
            for i in list(main.cwlist.keys()):
                if cmd.getname(i) not in wlistnames and main.cwlist[i] > 0:
                    wlistnames.append(cmd.getname(i))
            out.append(str(int(len(wlistnames)))
                       + ' whitelisted user(s).')
            out.append(str(len(c_wlist.adminlist)) + ' admin user(s).')
            if tolist:
                names = []
                cmd.outlist(["Whitelist:"] + wlistnames, 8)
                names = []
                for i in c_wlist.adminlist:
                    names.append(cmd.getname(i[1]))
                cmd.outlist(["Admins:"] + names, 8)
        if tochannels:
            out.append(str(len(main.ircprofiles[main.currentprofile]['channels'
                       ])) + ' channels.')
            if tolist:
                cmd.outlist(['Channels']
                            + main.ircprofiles[main.currentprofile]['channels'
                            ])
        if nothing:
            main.sendcmsg('No options will be used!')
        else:
            cmd.outlist(out)
        return True
    return False


def showhelp():
    main.sendcmsg(
        '.stats [-modules] [-users] [-channels] [-list]: Statistics of '
                   + c_net.name + '.')
