# -*- coding: utf-8 -*-
import configs.module
import configs.mload
import utils


def init():
    m = configs.module.Module('google')
    m.set_help('Get google results.')
    m.add_command_hook('google', {
        'function': google,
        'help': 'Get Google results.',
        'args': [
            {
                'name': 'num',
                'aliases': ['n'],
                'optional': True,
                'keyvalue': 'number',
                'help': 'Number of results (max 10).',
                },
            {
                'name': 'page',
                'optional': False,
                'help': 'Page to look for.',
                'end': True,
                },
            ]
        })
    m.add_command_alias('g', 'google')
    return m


def google(fp, args):
    google = fp.server.import_module('share.google', True)
    linkparse = fp.server.import_module('share.linkparse', True)
    try:
        n = min(int(args.getlinstr("num", "1")), 10)
    except TypeError:
        n = 1
    if n < 1:
        return "Asking for %d results probably won't get you anywhere." % n
    urls = []
    for url in google.search(
        args.getlinstr('page'), stop=2, only_standard=True):
        if len(urls) < n:
            urls.append("%s: <%s>" % (linkparse.get_title(url), url))
    if not urls:
        return "No results."
    return utils.ltos(urls, '; ')
