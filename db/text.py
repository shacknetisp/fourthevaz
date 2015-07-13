# -*- coding: utf-8 -*-
import ast
import pprint
import running
import os
from threading import Thread, Lock
import copy


class DB:
    """A text database object, saves in pprint format."""

    def __init__(self, filename, db=dict()):
        self.lock = Lock()
        """Register a DB object with <filename> and initialize with <db>."""
        self.filename = filename
        if self.filename not in running.dbs:
            running.dbs[self.filename] = db
        if self.filename not in running.locks:
            running.locks[self.filename] = Lock()

    def db(self):
        """Return the db object."""
        return running.dbs[self.filename]

    def load(self):
        """Load the db."""
        running.dbs[self.filename] = ast.literal_eval(
            open(self.filename).read())

    def save_thread(self, d):
        with running.locks[self.filename]:
            """Safe-save the db."""
            with open(self.filename + '.working', 'w') as f:
                f.write(pprint.pformat(d))
            try:
                os.unlink(self.filename)
            except:
                pass
            os.rename(self.filename + '.working', self.filename)

    def save(self):
        with running.locks[self.filename]:
            Thread(target=DB.save_thread, args=(self,
                copy.deepcopy(running.dbs[self.filename]),)).start()