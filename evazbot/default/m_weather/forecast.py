#
from base import *
weatherinfo = mload('m_weather.weatherinfo').weatherinfo
from prettytable import PrettyTable
import datetime
def getdate(num):
    if num == 1:
        return 'Monday'
    elif num == 2:
        return 'Tuesday'
    elif num == 3:
        return 'Wednesday'
    elif num == 4:
        return 'Thursday'
    elif num == 5:
        return 'Friday'
    elif num == 6:
        return 'Saturday'
    elif num == 7:
        return 'Sunday'


def printforecast(info, data, date):
    forecast = PrettyTable()
    headings = []
    for i in info:
        headings.append(i[0] + ' ' + i[1].strip('@'))
    forecast.field_names = ['Day'] + headings
    for day in data:
        if not date:
            datenums = day['@day'].split('-')
            weekdaynum = datetime.date(int(datenums[0]),int(datenums[1]),int(datenums[2])).isoweekday()
            tablerow = [getdate(weekdaynum)]
        elif date:
            datenums = day['@day']
            tablerow = [datenums]
        for i in info:
            tablerow.append(day[i[0]][i[1]])
        forecast.add_row(tablerow)
    return forecast.get_string()
