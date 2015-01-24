# -*- coding: utf-8 -*-
from base import *
import requests
import pint
from pint import UnitRegistry
ureg = UnitRegistry()


def start():
    return ["money", "unit"]


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
    elif ct.cmd("unit"):
        fromc = ct.args.get("from")
        toc = ct.args.get("to")
        try:
            amount = ct.args.getdef()
        except ValueError:
            amount = "1"
        Q_ = ureg.Quantity
        try:
            out = str(Q_(amount + "*" + fromc).to(toc))
            ct.msg('%s [%s] = %d [%s]' % (
                amount, fromc, round(float(out.split()[0]), int(
                    ct.args.get("round", "5"))), toc))
        except SyntaxError:
            ct.msg("Invalid input.")
        except pint.UndefinedUnitError:
            ct.msg("Invalid input.")
        except pint.unit.DimensionalityError:
            ct.msg("Invalid input.")


def showhelp(h):
    h("money -from=<curreny> -to=<currency> <amount>: Convert money.")
    h("unit -from=<unit> -to=<unit> -round=<digits> <amount>: Convert units.")