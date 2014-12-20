# -*- coding: utf-8 -*-
"""
#Use like this:

#Initialize:
import wordai
o = wordai.wordai("<your db file>")
o.load()

#Main AI function
textin = input()
print(o.process(textin))

#Get Dictionary Output
print(o.getdictstring())

#Replace a word
o.replace("old","new")

#It will auto-save to the database.
"""

from random import choice
import copy
import random
import string
import pprint
import ast


class wordai:
    dbfile = ''
    data_dict = {}

    def load(self):
        try:
            dict_file = open(self.dbfile, 'rb')
            self.data_dict = ast.literal_eval(dict_file.read().decode())
            dict_file.close()
        except:
            self.data_dict = {}
            pass

    def save(self):
        output = open(self.dbfile, 'w')
        output.write(pprint.pformat(self.data_dict))
        output.close()

    choices = list()

    def addchoice(self, a):
        self.choices.append(a)

    def ms(self, r):
        exclude = set(string.punctuation)
        r = ''.join(ch for ch in r if ch not in exclude)
        inp = r.lower().split()
        if len(inp):
            if not ';start' in self.data_dict:
                self.data_dict[';start'] = list()
            if not ';end' in self.data_dict:
                self.data_dict[';end'] = list()
            if not inp[0] in self.data_dict[';start'] or True:
                self.data_dict[';start'].append(inp[0])
            if not inp[-1] in self.data_dict[';end'] or True:
                self.data_dict[';end'].append(inp[-1])
        for i in range(len(inp)):
            if not inp[i] in self.data_dict:
                self.data_dict[inp[i]] = list()
            try:
                if not inp[i + 1] in self.data_dict[inp[i]] or True:
                    self.data_dict[inp[i]].append(inp[i + 1])
            except IndexError:
                pass
        ret = ''
        try:
            choices = list()
            for ch in range(4):
                try:
                    self.addchoice(choice(inp))
                except:
                    pass
            try:
                self.addchoice(inp[0])
            except:
                pass
            for ch in range(random.randrange(8, 16)):
                try:
                    self.addchoice(choice(self.data_dict[';start']))
                except:
                    pass
            try:
                self.addchoice(choice(self.data_dict[inp[0]]))
            except:
                pass
            first = choice(self.choices)
            ret += first + ' '
            nextword = first
            for numwords in range(100):
                if nextword in self.data_dict:
                    if nextword in self.data_dict[';end'] \
                        and (int(random.randrange(0, 100)) < 5 + numwords
                             + self.data_dict[';end'].count(nextword)
                             / len(self.data_dict[';end']) * 1000
                             or len(self.data_dict[nextword]) == 0):
                        break
                    cnext = choice(self.data_dict[nextword])
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

    def process(self, mp):
        self.load()
        out = self.ms(mp)
        self.save()
        return out

    def replace(self, w, n):
        if n != w:
            self.data_dict[n] = self.data_dict[w]
            del self.data_dict[w]
        for k in self.data_dict:
            for (index, item) in enumerate(self.data_dict[k]):
                if item == w:
                    self.data_dict[k][index] = n
        self.save()

    def getdictstring(self):
        self.load()
        data_dict_tmp = copy.deepcopy(self.data_dict)
        if ';record' in data_dict_tmp:
            del data_dict_tmp[';record']
        return pprint.pformat(data_dict_tmp)

    def getwords(self):
        self.load()
        data_dict_tmp = copy.deepcopy(self.data_dict)
        if ';record' in data_dict_tmp:
            del data_dict_tmp[';record']
        return len(data_dict_tmp) - 2

    def __init__(self, dbf):
        self.dbfile = dbf
