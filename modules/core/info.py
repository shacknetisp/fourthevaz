# -*- coding: utf-8 -*-
import configs.module
import version
import datetime
import time
import utils


def init():
    m = configs.module.Module(__name__)
    m.set_help('Get bot info and provide various CTCP functions.')
    m.add_command_hook('source',
        {
            'function': source,
            'help': 'Get link to source.',
            'args': [],
            })
    m.add_command_hook('gitver',
        {
            'function': gitver,
            'help': 'Git version.',
            'args': [
                {
                    'name': 'nolink',
                    'keyvalue': '',
                    'help': 'Do not display the link.',
                    'optional': True,
                    },
                ],
            })
    m.add_base_hook('ctcp.source', ctcp_source)
    m.add_command_hook('version',
        {
            'function': getversion,
            'help': 'Get version info.',
            'args': [],
            })
    m.add_base_hook('ctcp.version', ctcp_version)
    m.add_base_hook('ctcp.time', ctcp_time)
    m.add_command_hook('setuserinfo',
        {
            'function': setuserinfo,
            'help': 'Set the reply to CTCP USERINFO.',
            'args': [
                {
                    'name': 'text',
                    'optional': True,
                    'help': 'Text to reply with.',
                    'end': True,
                    },
                ],
            })
    m.add_short_command_hook(docs, "docs::Get link to the documentation", [])
    m.add_command_alias('documentation', 'docs')
    m.add_base_hook('ctcp.userinfo', ctcp_userinfo)
    m.add_base_hook('ctcp.clientinfo', ctcp_clientinfo)
    m.add_base_hook('ctcp.finger',
        lambda fp: fp.replyctcp('FINGER ' + fp.server.name))
    m.add_base_hook('ctcp.errmsg',
        lambda fp: fp.replyctcp('ERRMSG Invalid Data'))
    m.add_base_hook('apiaction', apiaction)
    return m


def source(fp, args):
    return version.source


def docs(fp, args):
    return version.docs


def apiaction(ret, server, q, environ, action):
    if action == 'info':
        del ret['message']
        ret['addr'] = server.entry['address']
        ret['channels'] = [
            c['channel'] for c in server.channels]
        ret['nicks'] = [
            name
            for c in server.channels
            for name in c['names']
            ]
        ret['modules'] = [
        (m.name, m.set)
        for m in server.modules
        ]
        ret['status'] = 'good'


def gitver(fp, args):
    if not version.gitstr():
        return 'Cannot find a git repository.'
    if 'nolink' in args.lin:
        return version.gitstr()
    return (version.gitstr() + ': ' +
    version.source + '/compare/%s...master' % (version.gitstr()) + ' ' +
    version.source + '/commit/%s' % (version.gitstr()))


def ctcp_source(fp):
    fp.replyctcp('SOURCE %s' % version.source)


def getversion(fp, args):
    return version.name + ' ' + version.versionstr()


def ctcp_version(fp):
    fp.replyctcp('VERSION %s %s (%s) | Python: %s | OS: %s' % (
        version.name,
        version.versionstr(),
        version.source,
        version.pythonversionstr(),
        version.systemversionstr(),
        ))


def ctcp_time(fp):
    val = (time.timezone / 60 / 60)
    fp.replyctcp('TIME ' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d %H:%M:%S GMT ') + str("" if val < 0 else "+") + str(
    val)))


def ctcp_userinfo(fp):
    try:
        if fp.server.db['userinfo']:
            fp.replyctcp('USERINFO %s' % fp.server.db['userinfo'])
            return
    except KeyError:
        pass
    fp.replyctcp('USERINFO <No reply set>')


def setuserinfo(fp, args):
    fp.server.db['userinfo'] = args.getlinstr('text', '<No reply set>')
    return 'CTCP USERINFO will now return "%s".' % fp.server.db['userinfo']


def ctcp_clientinfo(fp):
    fp.replyctcp('CLIENTINFO ' + utils.ltos(configs.module.ctcplist, " "))