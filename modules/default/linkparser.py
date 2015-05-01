# -*- coding: utf-8 -*-
import configs.module
import requests
import socket
URL_REGEX = r"""
\b
[http(s|)://]?
[.*]?[\.]?.*\..*
\b
"""
import re
linkparse = None


def init(options):
    global linkparse
    linkparse = options['server'].import_module('share.linkparse', True)
    m = configs.module.Module(__name__)
    m.set_help('Preform operations on links.')
    m.add_short_command_hook(title,
        'title::Get the title of a URL.', ['[url]::Url to view.'])
    m.add_base_hook('recv', recv)
    return m


def gettitle(url):
    title = ""
    try:
        try:
            title = linkparse.get_title(url, 2)
        except requests.exceptions.MissingSchema:
            url = 'http://' + url
            title = linkparse.get_title(url, 2)
    except requests.exceptions.ConnectionError:
        title = ""
    except socket.timeout:
        title = ""
    except requests.exceptions.Timeout:
        title = ""
    return title


def recv(fp):
    text = ""
    if fp.type == "irc":
        text = fp.sp.text
    elif fp.type == "file":
        text = fp.text
    try:
        find = re.findall(
            URL_REGEX.replace('\n', ''), text)[-1]
        if find.find('http') == -1 and find.count('.') < 2:
            return
        fp.server.state['lastlink.%s' % fp.outtarget()] = find
    except IndexError:
        pass


def title(fp, args):
    url = args.getlinstr('url',
        fp.server.state['lastlink.%s' % fp.outtarget()]
        if 'lastlink.%s' % fp.outtarget() in fp.server.state else
        None)
    title = gettitle(url)
    return title if title else 'Cannot find the title for %s.' % url