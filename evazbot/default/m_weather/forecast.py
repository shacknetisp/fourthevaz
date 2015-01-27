from base import *
weatherinfo = mload('m_weather.weatherinfo').weatherinfo
from prettytable import prettytable
from collections import OrderedDict
def printforecast(info, data):
    forecast = prettytable()
    headings = []
    for i in info:
        headings.append(i[0] + ' ' + i[1])
    forecast.field_names = headings
    for day in data:
        tablerow = [day['@day']]
        for i in info:
            tablerow.append(day[info[0]]['@' + info[1]])
        forecast.add_row(tablerow)
    return forecast.get_string()
