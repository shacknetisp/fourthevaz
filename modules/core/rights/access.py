# -*- coding: utf-8 -*-
accesslen = 3
hostidx = 1
import fnmatch
import copy
import utils


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


def splitchannel(right):
    if len(right.split(',')) == 2:
        return right.split(',')
    return []


def fullrights(fp, rights, r=True):
    ret = copy.deepcopy(rights)
    implied = {}
    for m in fp.server.modules:
        for ir in m.implicitrights:
            if ir not in implied:
                implied[ir] = []
            implied[ir] += m.implicitrights[ir]
    for right in rights:
        if splitchannel(right):
            gright = '%,' + splitchannel(right)[1]
            if gright in implied:
                for imp in implied[gright]:
                    if ('-' + imp.replace('%',
                    splitchannel(right)[0]).strip('-')) not in ret:
                        ret.append(imp.replace('%', splitchannel(right)[0]))
        else:
            if right in implied:
                for implication in implied[right]:
                    if splitchannel(implication) and fp.type == '':
                        if not fp.external():
                            for channel in fp.server.channels:
                                if 'names' in channel:
                                    if fp.sp.sendernick in channel['names']:
                                        if ('-' + (channel['channel'] +
                ',' + splitchannel(implication)[1]).strip('-')) not in ret:
                                            ret.append(channel['channel'] +
                                        ',' + splitchannel(implication)[1])
                    else:
                        if ('-' + implication.strip('-')) not in ret:
                            ret.append(implication)
    if r:
        oldrights = rights
        for i in range(10):
            if oldrights != ret:
                oldrights = copy.deepcopy(ret)
                ret = fullrights(fp, ret, False)
    return utils.unique(ret)


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