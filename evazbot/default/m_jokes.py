# -*- coding: utf-8 -*-

from base import *
import random
import os
import traceback

dbfolder = c_redeclipse.dbhome + '/jokes'


def msg(mp):
    if mp.wcmd('addjoke'):
        category = mp.argstr('c', 'joke')
        joke = mp.argsdef()
        if len(joke) < 1:
            main.sendcmsg('That is no joke.')
        else:
            dbfile = dbfolder + '/' + category
            dbfile += '.db.txt'
            with open(dbfile, 'a') as myfile:
                myfile.write(joke + '\n')
                main.sendcmsg("Joke added to category '" + category
                              + "': " + joke)
        return True
    if mp.cmd('joke'):
        target = ''
        try:
            target = mp.argsdef()
        except ValueError as e:
            main.sendcmsg(str(e)
                          + ' | Try enclosing <target> with "quotes"')
            return True
        except:
            traceback.print_exc()
        category = mp.argstr('c', 'joke')
        lines = []
        dbfile = dbfolder + '/' + category
        dbfile += '.db.txt'
        try:
            for line in open(dbfile, 'r'):
                if len(target) > 0 and line.find('#target#') != -1:
                    lines.append(line.strip())
                elif len(target) == 0 and line.find('#target#') == -1:
                    lines.append(line.strip())
        except IOError:
            main.sendcmsg('Invalid Category!')
        if len(lines) > 0:
            out = random.choice(lines)
        else:
            if target:
                out = \
                    '#caller# tried to play a joke on #target#, but failed.'
            else:
                out = '#caller# failed at joking.'
        out = out.replace('#target#', target)
        out = out.replace('#caller#', mp.user())
        main.sendcmsg(out)
        return True
    if mp.wcmd('sortjokes'):
        for (subdir, dirs, files) in os.walk(dbfolder):
            for fname in files:
                lines = []
                category = mp.argstr('c', 'joke')
                dbfile = os.path.join(subdir, fname)
                for line in open(dbfile, 'r'):
                    lines.append(line)
                    lines.sort()
                with open(dbfile, 'w') as f:
                    f.writelines(lines)
        main.sendcmsg('The jokes have been sorted.')
        return True
    if mp.cmd('jokecats'):
        jokecats = []
        for (subdir, dirs, files) in os.walk(dbfolder):
            for fname in files:
                targetcount = 0
                totalcount = 0
                for line in open(os.path.join(subdir, fname), 'r'):
                    if line.find('#target#') != -1:
                        targetcount += 1
                    totalcount += 1
                info = str(targetcount) + '/' + str(totalcount) \
                    + ' #target#'
                jokecats.append(fname.replace('.db.txt', '') + ': '
                                + info)
        cmd.outlist(jokecats)
        return True
    return False


def showhelp():
    main.sendcmsg(cmd.cprefix +
    'joke [-c=category] <target>: Recall a random joke, '
                  + 'with the target being <target>, ' +
                  'and the dbfile being <category>.'
                  )
    main.sendcmsg(
        cmd.cprefix +
        'addjoke [-c=<category>] <joke>: Add <the joke> to <category>. '
                  + '#target# will be replaced with the target of .joke,' +
                  '#caller# will be replaced with the caller of the joke.'
                  )
    main.sendcmsg(cmd.cprefix + 'sortjokes: Clean the DB.')
    main.sendcmsg(
        cmd.cprefix + 'jokecats: List all categories, ' +
        'with number of #target# and regular lines.'
                  )
