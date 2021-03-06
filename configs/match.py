# -*- coding: utf-8 -*-
import re
import fnmatch


def match(string, regex, fullmatch):
    """
    Match <string> to <regex> using a variety of matches.
    If <fullmatch> use str.find() as well.
    """
    a = None
    try:
        a = re.compile(regex)
    except re.error:
        pass
    return (a and a.match(string) is not None) or (
        not fullmatch and string.find(regex) != -1) or (
            fnmatch.fnmatch(string, regex))


def matchnocase(string, regex, fullmatch):
    """
    Match <string> to <regex> using a variety of matches.
    Use case-insensitivity.
    If <fullmatch> use str.find() as well.
    """
    a = None
    try:
        a = re.compile(regex, re.IGNORECASE)
    except re.error:
        pass
    return (a and a.match(string) is not None) or (
        not fullmatch and string.lower().find(regex.lower()) != -1) or (
            fnmatch.fnmatch(string.lower(), regex.lower()))