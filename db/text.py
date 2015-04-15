# -*- coding: utf-8 -*-
import ast
import pprint
import running
import os


class DB:
    """A text database object, saves in pprint format."""

    def __init__(self, filename, db=dict()):
        """Register a DB object with <filename> and initialize with <db>."""
        self.filename = filename
        if self.filename not in running.dbs:
            running.dbs[self.filename] = db

    def db(self):
        """Return the db object."""
        return running.dbs[self.filename]

    def load(self):
        """Load the db."""
        running.dbs[self.filename] = ast.literal_eval(
            open(self.filename).read())

    def save(self):
        """Safe-save the db."""
        with open(self.filename + '.working', 'w') as f:
            f.write(pprint.pformat(running.dbs[self.filename]))
        try:
            os.unlink(self.filename)
        except:
            pass
        os.rename(self.filename + '.working', self.filename)