# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, 'evazbot')
sys.path.insert(0, 'evazbot/modules')
sys.path.insert(0, 'evazbot/configs')
import main

modname = "IRC Ping"


def start():
    print(modname + " has started.")


def stop():
    print(modname + " has stopped")


def text(message):
    print(modname + " has recieved")


def ping():
    print(modname + " has pinged.")