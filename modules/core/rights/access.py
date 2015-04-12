# -*- coding: utf-8 -*-
accesslen = 3
hostidx = 1
import fnmatch
import copy


class AccessLevelError(Exception):

    def __init__(self, msg):
        super(AccessLevelError, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


def ischannel(u):
    if u:
        if u[0] == '#' and len(u.split()) == 1:
            return True
    return False


def raiseifnotformeduser(u):
    if ischannel(u):
        return
    if u.count('=') < accesslen - 1:
        raise AccessLevelError('The user %s is malformed!' % u)


def fullrights(fp, rights, r=True):
    ret = copy.deepcopy(rights)
    for m in fp.server.modules:
        for ir in m.implicitrights:
            irt = ''
            if len(ir.split(',')) == 2:
                if fp.channel:
                    irt = fp.channel.entry[
                        'channel'] + ',' + ir.split(',')[1]
            if ir in ret or irt in ret:
                for implied in m.implicitrights[ir]:
                    if len(implied.split(',')) == 2:
                        if fp.channel:
                            implied = fp.channel.entry[
                                'channel'] + ',' + implied.split(',')[1]
                    if implied not in ret:
                        ret.append(implied)
    if r:
        oldrights = rights
        for i in range(10):
            if oldrights != ret:
                oldrights = copy.deepcopy(ret)
                ret = fullrights(fp, ret, False)
    return ret


def getrights(server, user):
    rights = []
    raiseifnotformeduser(user)
    splitub = []
    splitu = ""
    if not ischannel(user):
        splitub = user.split('=')
        splitu = ["=".join(splitub[:-2]), splitub[-2], splitub[-1]]
    for l in [lambda x: x not in ['==', '#'], lambda x: x in ['==', '#']]:
        for k in server.adb:
            if not l(k):
                continue
            raiseifnotformeduser(k)
            good = True
            if ischannel(k):
                good = (k == user)
            else:
                if ischannel(user):
                    good = False
                else:
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
                for right in server.adb[k]:
                    if right.strip('-') not in rights and '-' + right.strip(
                        '-') not in rights:
                            rights.append(right)
    return rights


def setright(server, user, right):
    if user not in server.adb:
        server.adb[user] = {}
    sright = right.strip('-')
    dright = '-' + sright
    if sright in server.adb[user]:
        del server.adb[user][sright]
    if dright in server.adb[user]:
        del server.adb[user][dright]
    server.adb[user][right] = True


def delright(server, user, right):
    if user not in server.adb:
        server.adb[user] = {}
    if right in server.adb[user]:
        del server.adb[user][right]