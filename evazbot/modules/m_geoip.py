from base import * 
import pygeoip
import re
import socket
gi = pygeoip.GeoIP('pygeoip/GeoLiteCity.dat')

def msg(mp):
  if mp.isserver() and mp.text().find(") has joined the game (") != -1:
    ip = re.findall(' \((.*?)\) has', mp.text())[-1]
    try:
      r = gi.record_by_addr(ip)
    except:
      try:
        r = gi.record_by_name(ip)
      except:
        r = None
    try:
        index = mp.text().index(" ("+ip)
    except ValueError:
        index = len(s)
    try:
      main.sendcmsg(mp.text()[mp.text().index(" :")+2:index]+": "+r['country_name'])
      return True
    except TypeError:
      pass
    try:
      index = mp.text().index(" ("+ip)
    except ValueError:
      index = len(s)
    main.sendcmsg(mp.text()[mp.text().index(" :")+2:index]+": "+"Unknown")
    return True
  if mp.cmd("geoip"):
    ip = mp.argsdef()
    try:
      r = gi.record_by_addr(ip)
    except:
      try:
          r = gi.record_by_name(ip)
      except:
          r = None
    try:
      main.sendcmsg(r['city']+", "+r['region_code']+", "+r['country_name'])
    except TypeError:
      main.sendcmsg("Cannot get information.")
    return True
  return False

def showhelp():
  main.sendcmsg(".geoip <ip>: Find location information from IP address.")
