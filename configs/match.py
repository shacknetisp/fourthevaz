# -*- coding: utf-8 -*-
import re
import fnmatch


def match(string, regex, fullmatch):
    a = re.compile(regex)
    return (a.match(string) is not None) or (
        not fullmatch and string.find(regex) != -1) or (
            fnmatch.fnmatch(string, regex))


def matchnocase(string, regex, fullmatch):
    a = re.compile(regex, re.IGNORECASE)
    return (a.match(string) is not None) or (
        not fullmatch and string.lower().find(regex.lower()) != -1) or (
            fnmatch.fnmatchcase(string, regex))