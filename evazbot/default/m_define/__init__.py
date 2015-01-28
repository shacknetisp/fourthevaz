# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from base import *
import wikipedia
from urllib.request import urlopen
gtapi = mload("m_define.googletranslate")
import re
from html.parser import HTMLParser
search = mload("m_define.google").search


def start():
    return [
        'translate',
        'lookup',
        'define',
        'wiki',
        'google'
        ]


class MLStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def getwikipedia(word):
    try:
        output = wikipedia.summary(word, sentences=2)
    except wikipedia.exceptions.DisambiguationError as exc:
        output = wikipedia.summary(exc.options[0], sentences=2)
    return output


def getdictionary(word):
    html = \
        urlopen(
            'http://www.ibiblio.org/webster/cgi-bin/headword_search.pl?query='
                 + word.replace(' ', '+')).read().decode()
    s = re.sub(' +', ' ', cmd.find_between(html, '<def>', '</def>'
               ).strip()) + '.'
    return strip_tags(s)


def googleword(word, n=1):
    urls = []
    for url in search(word, stop=2, only_standard=True):
        if len(urls) < n:
            urls.append(str(url))
    cmd.outlist(urls)


def getl(l):
    ldict = {
        'en': ['english'],
        'de': ['german', 'deutsch'],
        'es': ['spanish', 'espanol', 'español'],
        'af': ['afrikaans'],
        'la': ['latin'],
        }
    for k, v in list(ldict.items()):
        if l.lower() in v:
            return k
    return l


def msg(mp):
    if mp.wcmd('google'):
        word = mp.args().strip()
        if not word:
            main.sendcmsg('Invalid Arguments!')
        googleword(mp.argsdef(), int(mp.argstr('n', '1')))
        if int(mp.argstr('n', '1')) <= 0:
            main.sendcmsg('Do you really expect results with a maximum of '
                           + str(int(mp.argstr('n', '1'))) + ' URLs?')
        return True
    if mp.wcmd('translate'):
        fromword = mp.argstr('from', '')
        toword = mp.argstr('to', 'en')
        translator = gtapi.TranslateService()
        if fromword == '':
            fromword = list(translator.detect(mp.argsdef()).keys())[0]
        main.sendcmsg(translator.trans_sentence(
                getl(fromword), getl(toword), mp.argsdef()))
        return True
    if mp.wcmd('define'):
        word = mp.args().strip()
        if not word:
            main.sendcmsg('Invalid Arguments!')
        main.sendcmsg(getdictionary(word))
        return True
    if mp.wcmd('wiki'):
        word = mp.args().strip()
        if not word:
            main.sendcmsg('Invalid Arguments!')
        output = ''
        try:
            output = getwikipedia(word)
        except wikipedia.exceptions.WikipediaException:
            output = 'Unable to locate definition...'
        main.sendcmsg(output)
        return True
    if mp.wcmd('lookup'):
        word = mp.args().strip()
        if not word:
            main.sendcmsg('Invalid Arguments!')
        googleword(word)
        try:
            output = getdictionary(word)
        except UnicodeEncodeError:
            output = '.'
        if output == '.' or len(output) < 1:
            try:
                output = getwikipedia(word)
            except wikipedia.exceptions.WikipediaException:
                output = 'Unable to locate definition...'
        main.sendcmsg(output)
        return True
    return False


def showhelp(h):
    h('translate -from=[language] -to=[language] <text>: Translate text. ' +
    'Leave -from empty to autodetect, -to defaults to english.')
    h('lookup <word>: Lookup <word>.')
    h('define <word>: Define <word>.')
    h('wiki <words>: Lookup on Wikipedia: <words>.')
    h('google [-n=number] <words to lookup>: Lookup on Google.')