# -*- coding: utf-8 -*-
import re


def contains(regex, string):
    a = re.compile(regex)
    return a.match(string) is not None


def casecontains(regex, string):
    a = re.compile(regex, re.IGNORECASE)
    return a.match(string) is not None