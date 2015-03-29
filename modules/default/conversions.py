# -*- coding: utf-8 -*-
import configs.module
import requests
import pint
from pint import UnitRegistry
ureg = UnitRegistry()


def init():
    m = configs.module.Module(__name__)
    m.set_help('Convert between units.')
    m.add_command_hook('money',
        {
            'help': 'Convert currency.',
            'function': money,
            'args': [
                {
                    'name': 'amount',
                    'optional': False,
                    'help': 'Amount of <from>.'
                    },
                        {
                    'name': 'from',
                    'optional': False,
                    'help': 'Convert from this.'
                    },
                        {
                    'name': 'to',
                    'optional': False,
                    'help': 'Convert to this.'
                    }
                ]
            })
    m.add_command_hook('convert',
        {
            'help': 'Convert units.',
            'function': convert,
            'args': [
                {
                    'name': 'amount',
                    'optional': False,
                    'help': 'Amount of <from>.'
                    },
                        {
                    'name': 'from',
                    'optional': False,
                    'help': 'Convert from this.'
                    },
                        {
                    'name': 'to',
                    'optional': False,
                    'help': 'Convert to this.'
                    }
                ]
            })
    return m


def money(fp, args):
    try:
        amount = float(args.getlinstr('amount'))
    except ValueError:
        return 'Invalid amount.'
    fromc = args.getlinstr('from').upper()
    toc = args.getlinstr('to').upper()
    response = requests.get(
        'http://www.freecurrencyconverterapi.com/api/v3/convert',
    params={'q': fromc + '_' + toc,
        'compact': 'ultra'}
    )
    json = response.json()
    print(json)
    try:
        rate = float(json[fromc + '_' + toc]) * amount
        return('Converting from %s %d: %s %.2f' % (
            fromc, amount, toc, round(rate, 2)))
    except KeyError:
        return("Invalid currency.")


def convert(fp, args):
    amount = args.getlinstr('amount')
    fromc = args.getlinstr('from').lower()
    toc = args.getlinstr('to').lower()
    Q_ = ureg.Quantity
    try:
        out = str(Q_(amount + "*" + fromc).to(toc))
        return('%s [%s] = %.5f [%s]' % (
        amount, fromc, round(float(out.split()[0]), 5), toc))
    except SyntaxError:
        return("Invalid input.")
    except pint.UndefinedUnitError:
        return("Undefined unit.")
    except pint.unit.DimensionalityError:
        return("Invalid input.")
    except ValueError:
        return("Invalid input.")