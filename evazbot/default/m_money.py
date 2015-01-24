# -*- coding: utf-8 -*-
from base import *
import requests


def start():
    return ["money"]


def get(ct):
    if ct.cmd("money"):
        fromc = ct.args.get("from", "USD")
        toc = ct.args.get("to", "USD")
        try:
            amount = float(ct.args.getdef())
        except ValueError:
            amount = 1
        response = requests.get(
            str('http://jsonrates.com/get/?' +
            'from=%s' +
            '&to=%s') % (fromc, toc)
        )
        json = response.json()
        try:
            rate = float(json['rate']) * amount
            ct.msg('Converting from %s %d: %s %.4f' % (
                fromc, amount, toc, round(rate, 4)))
        except KeyError:
            ct.msg("API error, invalid currency?")


def showhelp(h):
    h("money -from=<curreny> -to=<currency> <amount>: Convert money.")