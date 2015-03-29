# -*- coding: utf-8 -*-
from configs.module import Module
import os
import configs.locs
import datetime


def init():
    m = Module(__name__)
    m.set_help('Log messages.')
    m.add_base_hook('prerecv', recv)
    m.add_base_hook('output', output)
    m.add_base_hook('quit', doquit)
    m.add_base_hook('nick', donick)
    return m


def doquit(fp, channels):
    folder = configs.locs.userdata + '/logs/' + fp.server.entry['settings']
    os.makedirs(folder, exist_ok=True)
    for logname in channels + [fp.sp.sendernick]:
        with open(folder + '/' + logname, 'a') as f:
            f.write("[%s] <%s> %s\n" % (
                datetime.datetime.utcnow(),
                fp.sp.sendernick, fp.sp.message.strip()))


def donick(fp, channels):
    folder = configs.locs.userdata + '/logs/' + fp.server.entry['settings']
    os.makedirs(folder, exist_ok=True)
    for logname in channels + [fp.sp.sendernick]:
        with open(folder + '/' + logname, 'a') as f:
            f.write("[%s] <%s> %s\n" % (
                datetime.datetime.utcnow(),
                fp.sp.sendernick, fp.sp.message.strip()))


def recv(fp):
    folder = configs.locs.userdata + '/logs/' + fp.server.entry['settings']
    os.makedirs(folder, exist_ok=True)
    if not fp.outtarget() or fp.outtarget() == '*' or fp.outtarget()[0] == ':':
        with open(folder + '/' + 'serv.er', 'a') as f:
            f.write("[%s] <%s> %s\n" % (
            datetime.datetime.utcnow(),
            fp.sp.sendernick, fp.sp.message.strip()))
        return
    text = fp.sp.text.strip()
    with open(folder + '/' + fp.outtarget(), 'a') as f:
        if text:
            f.write("[%s] <%s> %s\n" % (
                datetime.datetime.utcnow(), fp.sp.sendernick, text))
        else:
            f.write("[%s] <%s> %s\n" % (
                datetime.datetime.utcnow(),
                fp.sp.sendernick, fp.sp.message.strip()))


def output(fp, target, message):
    folder = configs.locs.userdata + '/logs/' + fp.server.entry['settings']
    os.makedirs(folder, exist_ok=True)
    with open(folder + '/' + target, 'a') as f:
        f.write("[%s] <%s> %s\n" % (
            datetime.datetime.utcnow(), fp.server.nick, message.strip()))
