#!/usr/bin/python
# -*- coding: utf-8 -*-

from base import *
import pickle

dbfile = c_redeclipse.dbhome + '/faq.db.pkl'

data_dict = {}


def load():
    global data_dict
    try:
        dict_file = open(dbfile, 'rb')
        data_dict = pickle.load(dict_file)
        dict_file.close()
    except:
        pass


def save():
    global data_dict
    output = open(dbfile, 'wb')
    pickle.dump(data_dict, output)
    output.close()


def msg(mp):
    if mp.cmd('faq'):
        load()
        if mp.argbool('add'):
            if not mp.iswlist():
                main.sendcmsg('You are not authorized.')
                return True
            data_dict[mp.argstr('add').strip()] = mp.argsdef('')
            main.sendcmsg('Added: ' + mp.argstr('add'))
        elif mp.argbool('remove'):
            if not mp.iswlist():
                main.sendcmsg('You are not authorized.')
                return True
            try:
                del data_dict[mp.argstr('remove').strip()]
                main.sendcmsg('Removed: ' + mp.argstr('remove'))
            except KeyError:
                main.sendcmsg("You can't delete something that isn't there."
                              )
        elif mp.argbool('list'):
            keys = []
            for i in list(data_dict.keys()):
                if i.find(mp.argstr('list').strip()) == 0:
                    keys.append(i)
            cmd.outlist(keys)
        else:
            try:
                main.sendcmsg(data_dict[mp.args().strip()])
            except KeyError:
                main.sendcmsg('That FAQ does not exist.')
        save()
    return False


def showhelp():
    main.sendcmsg(cmd.cprefix() + 'faq <name>')
    main.sendcmsg(cmd.cprefix() + 'faq -list=<prefix>')
    main.sendcmsg(cmd.cprefix() + 'faq -add=<name> <content>')
    main.sendcmsg(cmd.cprefix() + 'faq -remove=<name>')
