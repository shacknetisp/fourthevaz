# -*- coding: utf-8 -*-
"""
#Use like this:

#Initialize:
import wordai
wordai.dbfile = "<your db file>"
wordai.load()

#Main AI function
textin = input()
print(wordai.process(textin))

#Get Dictionary Output
print(wordai.getdictstring())

#Replace a word
wordai.replace("old","new")

#It will auto-save to the database.
"""

from random import choice
import random
import string
import pickle
import pprint

dbfile = ''

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


choices = list()


def addchoice(a):
    choices.append(a)


def ms(r):
    global choices
    global data_dict
    exclude = set(string.punctuation)
    r = ''.join(ch for ch in r if ch not in exclude)
    inp = r.lower().split()
    if len(inp):
        if not ';start' in data_dict:
            data_dict[';start'] = list()
        if not ';end' in data_dict:
            data_dict[';end'] = list()
        if not inp[0] in data_dict[';start'] or True:
            data_dict[';start'].append(inp[0])
        if not inp[-1] in data_dict[';end'] or True:
            data_dict[';end'].append(inp[-1])
    for i in range(len(inp)):
        if not inp[i] in data_dict:
            data_dict[inp[i]] = list()
        try:
            if not inp[i + 1] in data_dict[inp[i]] or True:
                data_dict[inp[i]].append(inp[i + 1])
        except IndexError:
            pass
    ret = ''
    try:
        choices = list()
        for ch in range(4):
            try:
                addchoice(choice(inp))
            except:
                pass
        try:
            addchoice(inp[0])
        except:
            pass
        for ch in range(random.randrange(8, 16)):
            try:
                addchoice(choice(data_dict[';start']))
            except:
                pass
        try:
            addchoice(choice(data_dict[inp[0]]))
        except:
            pass
        first = choice(choices)
        ret += first + ' '
        nextword = first
        for numwords in range(100):
            if nextword in data_dict:
                if nextword in data_dict[';end'] \
                    and (int(random.randrange(0, 100)) < 5 + numwords
                         + data_dict[';end'].count(nextword)
                         / len(data_dict[';end']) * 1000
                         or len(data_dict[nextword]) == 0):
                    break
                cnext = choice(data_dict[nextword])
                ret += cnext + ' '
                nextword = cnext
            else:
                break
    except IndexError:
        pass
    except KeyError:
        pass
    try:
        return str(str(ret[0]).upper() + ret[1:]).strip() + '.'
    except IndexError:
        return '?'


def process(mp):
    global data_dict
    load()
    out = ms(mp)
    save()
    return out


def replace(w, n):
    global data_dict
    if n != w:
        data_dict[n] = data_dict[w]
        del data_dict[w]
    for k in data_dict:
        for (index, item) in enumerate(data_dict[k]):
            if item == w:
                data_dict[k][index] = n
    output = open(dbfile, 'wb')
    pickle.dump(data_dict, output)
    output.close()


def getdictstring():
    global data_dict
    load()
    data_dict_tmp = list(data_dict)
    if ';record' in data_dict_tmp:
        del data_dict_tmp[';record']
    return pprint.pformat(data_dict_tmp)


def getwords():
    global data_dict
    load()
    data_dict_tmp = list(data_dict)
    if ';record' in data_dict_tmp:
        del data_dict_tmp[';record']
    return len(data_dict_tmp) - 2
