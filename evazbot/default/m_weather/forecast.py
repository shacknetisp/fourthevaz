#
from base import *
weatherinfo = mload('m_weather.weatherinfo').weatherinfo
from prettytable import PrettyTable


def printforecast(info, data):
    forecast = PrettyTable()
    headings = []
    for i in info:
        headings.append(i[0] + ' ' + i[1].strip('@'))
    forecast.field_names = ['Day'] + headings
    for day in data:
        tablerow = [day['@day']]
        for i in info:
            tablerow.append(day[i[0]][i[1]])
        forecast.add_row(tablerow)
    return forecast.get_string()
