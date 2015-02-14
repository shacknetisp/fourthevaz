# -*- coding: utf-8 -*-
import pickle
import os


class variablestore:
    dbfile = ''
    data_dict = {}

    def load(self):
        dict_file = open(self.dbfile, 'rb')
        try:
            self.data_dict = pickle.load(dict_file)
        except:
            pass
        dict_file.close()

    def save(self):
        output = open(self.dbfile + '.working', 'wb')
        pickle.dump(self.data_dict, output)
        output.close()
        try:
            os.unlink(self.dbfile)
        except:
            pass
        os.rename(self.dbfile + '.working', self.dbfile)

    def setvar(self, v, val):
        self.data_dict[str(v)] = str(val)

    def getvarstr(self, v, default=""):
        try:
            return self.data_dict[str(v)]
        except KeyError:
            return default

    def getvarnum(self, v, default=0):
        return float(self.getvarstr(v, str(default)))

    def defaultvar(self, v, val):
        if v not in self.data_dict:
            self.setvar(v, val)

    def __init__(self, dbf):
        self.dbfile = dbf


class liststore:
    dbfile = ''
    data_list = []

    def load(self):
        dict_file = open(self.dbfile, 'rb')
        try:
            self.data_list = pickle.load(dict_file)
        except:
            pass
        dict_file.close()

    def save(self):
        output = open(self.dbfile + '.working', 'wb')
        pickle.dump(self.data_list, output)
        output.close()
        try:
            os.unlink(self.dbfile)
        except:
            pass
        os.rename(self.dbfile + '.working', self.dbfile)

    def __init__(self, dbf):
        self.dbfile = dbf