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
          earchari = random.randrange(min(len(earcharsl),len(earcharsr)))
          main.sendcmsg(earcharsl[earchari]+id_generator(1,eyechars)+id_generator(1,mouthchars)+id_generator(1,eyechars)+earcharsr[earchari])
          return True
    return False
