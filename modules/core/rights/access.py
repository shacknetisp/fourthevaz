# -*- coding: utf-8 -*-
import running
accesslen = 3
hostidx = 1
import fnmatch


class AccessLevelError(Exception):

    def __init__(self, msg):
        super(AccessLevelError, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


def raiseifnotformeduser(u):
    if u.count('=') < accesslen - 1:
        raise AccessLevelError('The user %s is malformed!' % u)


def getaccesslevel(server, user, alist="", channel=None, ltn=False):
    highest = 0
    lowest = 0
    splitub = user.split('=')
    splitu = ["=".join(splitub[:-2]), splitub[-2], splitub[-1]]
    raiseifnotformeduser(user)
    for l in server.entry['access']:
        if alist and l != alist:
            continue
        d = running.accesslist.db()[l]
        for k in d:
            raiseifnotformeduser(k)
            splitkb = k.split('=')
            splitk = ["=".join(splitkb[:-2]), splitkb[-2], splitkb[-1]]
            good = True
            for i in range(accesslen):
                if splitk[i]:
                    if (splitk[i] == splitu[i] or (
                        i == hostidx and fnmatch.fnmatchcase(
                            splitu[i], splitk[i]))) and good:
                        good = True
                    else:
                        good = False
            if good:
                lowest = min(lowest, d[k])
                highest = max(highest, d[k])
    if channel and (not alist or alist == server.entry['access'][0] + '=' +
    channel.entry['channel']) and not ltn:
        if splitu[0] in server.whoislist:
            if channel.entry['channel'] in server.whoislist[splitu[0]]['op']:
                highest = max(highest, 50)
            elif channel.entry[
                'channel'] in server.whoislist[splitu[0]]['voice']:
                highest = max(highest, 25)
    if lowest < 0:
        return lowest
    return highest


def setaccesslevel(alist, user, level):
    raiseifnotformeduser(user)
    try:
        d = running.accesslist.db()[alist]
    except KeyError:
        raise AccessLevelError('Invalid alist.')
    d[user] = level
    if level == 0:
        del d[user]
    running.accesslist.save()