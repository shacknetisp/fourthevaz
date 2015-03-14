# -*- coding: utf-8 -*-
import running
accesslen = 3
hostidx = 1
import fnmatch


class AccessLevelError(Exception):

    def __init__(self, msg):
        super(AccessLevelError, self).__init__()
        self.msg = msg


def raiseifnotformeduser(u):
    splitu = u.split(':')
    if len(splitu) != accesslen:
        raise AccessLevelError('The user %s is malformed!' % u)


def getaccesslevel(server, user, alist=""):
    highest = 0
    splitu = user.split(':')
    raiseifnotformeduser(user)
    for l in server.entry['access']:
        if alist and l != alist:
            continue
        d = running.accesslist.db[l]
        for k in d:
            raiseifnotformeduser(k)
            splitk = k.split(':')
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
                highest = max(highest, d[k])
    return highest


def setaccesslevel(alist, user, level):
    raiseifnotformeduser(user)
    try:
        d = running.accesslist.db[alist]
    except KeyError:
        raise AccessLevelError('Invalid alist.')
    d[user] = level
    if level == 0:
        del d[user]
    running.accesslist.save()