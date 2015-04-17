# -*- coding: utf-8 -*-
import xml.sax.saxutils


def remove_indices(l, indices):
    """Return <l> with <indices> removed."""
    result = []
    i = 0
    for j in sorted(indices):
        result += l[i:j]
        i = j + 1
    result += l[i:]
    return result


def unique(seq, idfun=None):
    """
    Return <seq> with no elements the same.
    Transform each element with <idfun(x)> before comparing."""
    if idfun is None:
        def idfun(x):
            return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)
    return result


def ltos(l, d=', '):
    """Same as d.join(l), but converting l's elements to str() beforehand."""
    out = []
    for i in l:
        out.append(str(i))
    return d.join(out)


def find_between(s, first, last):
    """Return first text in s between <first> and <last>."""
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def strip_html_tags(html):
    """Strip HTML tags from a str."""
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
    """Strip XML ampcodes from a str."""
    return xml.sax.saxutils.unescape(text)


def merge_dicts(*dict_args):
    """Return a merged dictionary from <dict_args>"""
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def boolstr(s):
    """Return a str converted to a bool using a list of truth values."""
    if s.lower() in ['yes', 'y', 'true', 't', '1']:
        return True
    elif s.lower() in ['no', 'n', 'false', 'f', '0']:
        return False
    else:
        raise ValueError('Invalid boolean value.')


def utcepoch():
    """Get the UTC epoch time."""
    import datetime
    dt = datetime.datetime.utcnow()
    return dt.timestamp()


class time:
    """Time related functions"""

    def durstr(dur):
        """Return dur as a formatted string."""
        ret = ""
        for style in [
            (60 * 60 * 24 * 7, 'w'),
            (60 * 60 * 24, 'd'),
            (60 * 60, 'h'),
            (60, 'm'),
            (1, 's'),
            ]:
                amount = dur // style[0]
                extra = dur % style[0]
                dur = extra
                if amount > 0:
                    ret += '%d%s' % (amount, style[1])

        return ret if ret else '???'

    def ago(ts):
        """Return durstr(utcepoch() - ts)."""
        return time.durstr(utcepoch() - ts)