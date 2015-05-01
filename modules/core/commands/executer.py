# -*- coding: utf-8 -*-
import os
import fnmatch
import subprocess


def execute(server, name, args, env):
    for path in server.modulepaths():
        for f in os.listdir(path):
            if fnmatch.fnmatch(f, '%s.ext' % name):
                return subprocess.check_output([path + '/' + f],
                     input=args.encode(),
                     shell=True,
                     env=env).decode().strip()
    return None