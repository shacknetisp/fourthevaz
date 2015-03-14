# -*- coding: utf-8 -*-
import ast
import pprint


class DB:

    def __init__(self, filename="", db=dict()):
        self.filename = filename
        self.db = db

    def load(self, filename=""):
        if filename:
            self.filename = filename
        self.db = ast.literal_eval(open(self.filename).read())

    def save(self, filename=""):
        if filename:
            self.filename = filename
        open(self.filename, 'w').write(pprint.pformat(self.db))