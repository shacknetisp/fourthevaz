# -*- coding: utf-8 -*-
from random import choice
import copy
import random
import string
import pprint
import pickle


class wordai:
    """Word AI"""

    def load(self):
        """Load the file."""
        try:
            self.dict_file = open(self.dbfile, 'rb')
            self.data_dict = pickle.load(self.dict_file)
            self.dict_file.close()
        except:
            pass

    def save(self):
        """Save the file"""
        output = open(self.dbfile, 'wb')
        pickle.dump(self.data_dict, output)
        output.close()

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
            self.choices = list()
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
        """Process <mp> and return a reply."""
        out = self.ms(mp)
        self.save()
        return out

    def replace(self, w, n):
        """Replace <w> with <n> in the dictionary."""
        if n != w:
            self.data_dict[n] = self.data_dict[w]
            del self.data_dict[w]
        for k in self.data_dict:
            for (index, item) in enumerate(self.data_dict[k]):
                if item == w:
                    self.data_dict[k][index] = n
        self.save()

    def getdictstring(self):
        """Return the pprinted dictionary."""
        data_dict_tmp = copy.deepcopy(self.data_dict)
        if ';record' in data_dict_tmp:
            del data_dict_tmp[';record']
        return pprint.pformat(data_dict_tmp)

    def getwords(self):
        """Get the number of words."""
        data_dict_tmp = copy.deepcopy(self.data_dict)
        if ';record' in data_dict_tmp:
            del data_dict_tmp[';record']
        return len(data_dict_tmp) - 2

    def __init__(self, dbf):
        self.dbfile = dbf
        self.choices = []
