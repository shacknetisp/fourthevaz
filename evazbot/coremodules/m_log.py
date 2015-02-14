# -*- coding: utf-8 -*-

from base import *
import datetime
import time


def dbfolder(dcc=False):
    df = c_redeclipse.dbhome + '/logs/' + c_wlist.wname()
    if dcc:
        df = c_redeclipse.dbhome + '/logs/dcc'
    return df


def msg(mp):
    mkpath(dbfolder())
    loc = mp.text().find(' :') + len(' :')
    st = \
        datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S'
            )
    fout = '[' + st + '] ' + '<' + mp.ircuser() + '> ' + mp.text()[loc:]
    if len(mp.text()[loc:]) > 0:
        cname = main.getchannel()
        cname = cname.replace('#', '')
        if cname == main.ircprofiles[main.currentprofile]['nick']:
            cname = main.getuser()
        with open(dbfolder() + '/' + cname + '.channel', 'a') as f:
            f.write(fout + '\n')


def dccget(dcc, text):
    mkpath(dbfolder(True))
    st = \
        datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S'
            )
    fout = '[' + st + '] ' + '<' \
        + dcc.nick + '> ' \
        + text
    if len(main.outputtext) > 0:
        cname = dcc.nick
        with open(dbfolder(True) + '/' + cname + '.dcc', 'a') as f:
            f.write(fout + '\n')


def dccout(dcc, text):
    mkpath(dbfolder(True))
    st = \
        datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S'
            )
    fout = '[' + st + '] ' + '<' \
        + main.ircprofiles[dcc.profile]['nick'] + '> ' \
        + text
    print(text)
    if len(main.outputtext) > 0:
        cname = dcc.nick
        with open(dbfolder(True) + '/' + cname + '.dcc', 'a') as f:
            f.write(fout + '\n')


def output():
    mkpath(dbfolder())
    st = \
        datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S'
            )
    fout = '[' + st + '] ' + '<' \
        + main.ircprofiles[main.currentprofile]['nick'] + '> ' \
        + main.outputtext
    if len(main.outputtext) > 0:
        cname = main.outputchannel
        cname = cname.replace('#', '')
        with open(dbfolder() + '/' + cname + '.channel', 'a') as f:
            f.write(fout + '\n')
