# -*- coding: utf-8 -*-
import xml.sax.saxutils


def remove_indices(l, indices):
    result = []
    i = 0
    for j in sorted(indices):
        result += l[i:j]
        i = j + 1
    result += l[i:]
    return result


def ltos(l, d=', '):
    out = []
    for i in l:
        out.append(str(i))
    return d.join(out)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def strip_html_tags(html):
    from html.parser import HTMLParser

    class MLStripper(HTMLParser):

        def __init__(self):
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.fed = []

        def handle_data(self, d):
            self.fed.append(d)

        def get_data(self):
            return ''.join(self.fed)

    s = MLStripper()
    s.feed(html)
    if s.get_data():
        return s.get_data()
    else:
        return html


def strip_xml_ampcodes(text):
    return xml.sax.saxutils.unescape(text)


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def boolstr(s):
    if s.lower() in ['yes', 'y', 'true', 't', '1']:
        return True
    elif s.lower() in ['no', 'n', 'false', 'f', '0']:
        return False
    else:
        raise ValueError('Invalid boolean value.')


def utcepoch():
    import datetime

    dt = datetime.datetime.utcnow()

    return dt.timestamp()