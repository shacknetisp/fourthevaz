from base import *
import string
import random
earcharsl = "<([{!/\\'\""
earcharsr = ">)]}!\\/'\""
eyechars = "*oO0$^"
mouthchars = "._-~"
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def msg(mp):
    if mp.cmd("..") or mp.cmd("") or mp.cmd("."):
          earchari = random.randrange(int(-(min(len(earcharsl),len(earcharsr))*0.5)),min(len(earcharsl),len(earcharsr)))
          if earchari >= 0:
            main.sendcmsg(earcharsl[earchari]+id_generator(1,eyechars)+id_generator(1,mouthchars)+id_generator(1,eyechars)+earcharsr[earchari])
          else:
            main.sendcmsg(id_generator(1,eyechars)+id_generator(1,mouthchars)+id_generator(1,eyechars))
          return True
    return False
