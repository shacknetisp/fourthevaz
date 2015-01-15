# -*- coding: utf-8 -*-
import re
from base import *
import random


class quotedb:

    def __init__(self, db, index, singular, plural, ct):
        self.db = db
        self.index = index
        self.singular = singular
        self.plural = plural
        self.ct = ct
        if index not in self.db.data_dict:
            self.db.data_dict[index] = []

    def add(self, inp, w=0, a=0, v=True):
        if self.ct.islogin(w, a, v):
            if inp not in self.db.data_dict[self.index]:
                self.db.data_dict[self.index].append(inp)
                self.ct.msg('Added ' + self.singular + ': ' + inp)
                self.db.save()
            else:
                self.ct.msg('That ' + self.singular + ' already exists.')

    def remove(self, search, w=0, a=0, v=True):
        if self.ct.islogin(w, a, v):
            limit = 0
            removedone = False
            try:
                for i in range(len(self.db.data_dict[self.index])):
                    if c_regex.casecontains(
                        search, self.db.data_dict[self.index][i]) and len(
                            self.db.data_dict[self.index][i]) > 0 and len(
                            search) > 0:
                        limit += 1
                        if limit < 5:
                            self.ct.msg('Removed ' + self.singular + ': ' +
                            self.db.data_dict[self.index][i])
                            self.db.data_dict[self.index][i] = ''
                            removedone = True
                        else:
                            self.ct.msg('Limit reached to delete at one time.')
                            break
            except re.error as e:
                self.ct.msg('Error: ' + str(e))
            if not removedone:
                self.ct.msg('No matching ' + self.plural + ' were found.')
            else:
                self.db.save()

    def get(self, search, musthave='', mustnothave=''):
        choices = []
        try:
            for i in range(len(self.db.data_dict[self.index])):
                if (self.db.data_dict[self.index][i].lower().find(
                    search.lower()) != -1 or c_regex.casecontains(
                        search, self.db.data_dict[self.index][i])) and len(
                            self.db.data_dict[self.index][i]) > 0:
                    choice = self.db.data_dict[self.index][i]
                    if len(musthave) == 0 or choice.lower().find(
                        musthave) != -1:
                        if len(mustnothave) == 0 or choice.lower().find(
                        mustnothave) == -1:
                            choices.append(choice)
        except re.error as e:
            self.ct.msg('Error: ' + str(e))
        if len(choices) == 0:
            self.ct.msg('No matches.')
            return None
        else:
            return(random.choice(choices))