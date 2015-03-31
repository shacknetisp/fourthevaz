# -*- coding: utf-8 -*-
import ast
import pprint
import running
import os


class DB:

    def __init__(self, filename, db=dict()):
        self.filename = filename
        if self.filename not in running.dbs:
            running.dbs[self.filename] = db

    def db(self):
        return running.dbs[self.filename]

    def load(self):
        running.dbs[self.filename] = ast.literal_eval(
            open(self.filename).read())

    def save(self):
        with open(self.filename + '.working', 'w') as f:
            f.write(pprint.pformat(running.dbs[self.filename]))
        try:
            os.unlink(self.filename)
        except:
            pass
        os.rename(self.filename + '.working', self.filename)