# -*- coding: utf-8 -*-
from json import loads
from urllib.request import urlopen
from decimal import *


class weatherinfo:
    data = {}

    def getinfo(self, info):
        data = self.data
        name = data["name"]
        cname = data["sys"]["country"]
        if len(name) == 0:
            name = self.dname
        #checks what the request wants
        if info == "temp":
            if self.outputtemp == "kel":
                return "It is " +\
                str(data["main"]["temp"]) +\
                " Kelvin in " + name + ", " + cname
            elif self.outputtemp == "cel":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                return "It is " + str(temp) +\
                " Celcius in " + name + ", " + cname
            elif self.outputtemp == "far":
                temp = Decimal(str(data["main"]["temp"])) - Decimal('273.15')
                temp = Decimal(str(temp)) * Decimal('1.8') + Decimal('32.0')
                return "It is " + str(temp) +\
                " Farenheit in " + name + ", " + cname
            else:
                raise ValueError(
                    "Invalid Temperature Style: " + self.outputtemp)
        elif info == "windspe":
            return "The Wind is Blowing at " +\
            str(data["wind"]["speed"]) + " m/s in " + name + ", " + cname

    def __init__(self, url, style, altname):
        jsonobj = urlopen(url)
        jsonobj = jsonobj.read()
        self.data = loads(jsonobj.decode())
        self.outputtemp = style
        self.dname = altname
