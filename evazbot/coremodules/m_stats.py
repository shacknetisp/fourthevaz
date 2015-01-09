# -*- coding: utf-8 -*-

from base import *


def msg(mp):
    if mp.cmd('stats'):
        out = []
        custom_count = 0
        default_count = 0
        for i in c_modules.module_callbacks:
            if i[c_modules.custom_offset]:
                custom_count += 1
            else:
                default_count += 1
        tolist = mp.argbool('list')
        tomodules = mp.argbool('modules')
        tousers = mp.argbool('users')
        tochannels = mp.argbool('channels')
        nothing = not tomodules and not tousers and not tochannels
        if tomodules:
            out.append("Module set: " + main.moduleset)
            m_totalstr = str(len(c_modules.module_callbacks))
            out.append(str(default_count) + '/' + m_totalstr
                       + ' set/all modules.')
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
            out.append("Whitelist: " +
            main.ircprofiles[main.currentprofile]['whitelist'])
            out.append(str(len(c_wlist.getw("whitelist")) +
            len(c_wlist.getcwlist())) +
            ' whitelist nick(s).')
            out.append(str(len(c_wlist.getw("adminlist"))) + ' admin user(s).')
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
