# -*- coding: utf-8 -*-
from configs.module import Module
import running
import configs.locs
import version


def init():
    m = Module(__name__)
    m.set_help('Write status output.')
    m.add_timer_hook(15 * 1000, timer)
    return m


def timer():
    html = open(configs.locs.userdata + '/status.html', 'w')
    txt = open(configs.locs.userdata + '/status.txt', 'w')

    def outputline(l):
        html.write(l.replace(' ', '&nbsp') + '<br>\n')
        txt.write(l + '\n')
    html.write('<h1>%s Status</h1>' % version.name)
    outputline('%d Servers:' % len(running.working_servers))
    for server in running.working_servers:
        if server.type == 'irc':
            outputline(' %s:%d %s (%s:%s)' % (
                server.entry['address']['host'],
                server.entry['address']['port'],
                server.entry['settings'],
                server.entry['id']['nick'],
                server.entry['id']['name'],
                ))
            for channel in server.channels:
                outputline('  %s' % channel['channel'])
                if 'names' in channel:
                    for name in channel['names']:
                        outputline('   %s' % name)
