# -*- coding: utf-8 -*-
import ast
import pprint
dbs = {}


class DB:

    def __init__(self, filename, db=dict()):
        self.filename = filename
        if self.filename not in dbs:
            dbs[self.filename] = db

    def db(self):
        return dbs[self.filename]

    def load(self):
        dbs[self.filename] = ast.literal_eval(open(self.filename).read())

    def save(self):
        open(self.filename, 'w').write(pprint.pformat(dbs[self.filename]))