# -*- coding: utf-8 -*-
import utils
import configs.module
import urllib.request
import urllib.parse
import xmltodict
import random
import re


def init():
    m = configs.module.Module('define')
    m.set_help('Get dictionary definitions.')
    m.add_command_hook('define', {
        'function': define,
        'help': 'Get a dictionary definition from ' +
        'http://www.onelook.com and http://www.ibiblio.org/',
        'args': [
            {
                'name': 'words',
                'optional': False,
                'help': 'Word(s) to look for.',
                'end': True,
                },
            ]
        })
    m.add_command_alias('d', 'define')
    return m


def getibiblio(word):
    html = \
    urllib.request.urlopen(
    'http://www.ibiblio.org/webster/cgi-bin/headword_search.pl?query='
    + word.replace(' ', '+')).read().decode()
    s = re.sub(' +', ' ', utils.find_between(html, '<def>', '</def>'
    ).strip()) + '.'
    return utils.strip_html_tags(s)


def define(fp, args):
    def sanitize(s):
        s = utils.strip_xml_ampcodes(s)
        hs = utils.strip_html_tags(s)
        if hs:
            return hs.replace('\n', '')
        return s.replace('\n', '')
    rawdata = urllib.request.urlopen(
            "http://www.onelook.com/?w=%s&xml=1" % urllib.parse.quote_plus(
                args.getlinstr(
                'words'))).read()
    data = xmltodict.parse(rawdata)
    try:
        try:
            qd = data['OLResponse']['OLQuickDef']
        except TypeError:
            raise KeyError
        if type(qd) is str:
            return sanitize(qd)
        return sanitize(qd[0]) + ' --- ' + sanitize(random.choice(qd[1:]))
    except KeyError:
        ibiblio = getibiblio(urllib.parse.quote_plus(
                args.getlinstr(
                'words')))
        if ibiblio and ibiblio != '.':
            return ibiblio.replace('\n', '')
        return "No definition found."
