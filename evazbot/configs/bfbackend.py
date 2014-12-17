#!/usr/bin/python3
#
# Brainf**k Interpreter
# Copyright 2011 Sebastian Kaspari
#

from base import *

def evaluate(code,intextp):
  intext = intextp
  code     = list(cleanup(list(code)))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr, outputlist = [0], 0, 0, []

  timesrun = 0

  while codeptr < len(code):
    timesrun += 1
    if timesrun > 10000:
        main.sendcmsg("Max loop met.")
        return "".join(outputlist)
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": outputlist.append(chr(cells[cellptr]))
    if command == ",":
        try:
            cells[cellptr] = ord(intext[0])
            intext = intext[1:]
        except IndexError:
            cells[cellptr] = ord(chr(0))

    codeptr += 1
  return "".join(outputlist)

def cleanup(code):
  return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code)


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


