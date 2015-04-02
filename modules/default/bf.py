# -*- coding: utf-8 -*-
import configs.module


def init(options):
    options['server'].state['bf.input'] = ""
    m = configs.module.Module(__name__)
    m.set_help('Execute Brainf**k.')
    m.add_command_hook('bf',
        {
            'function': bf,
            'help': 'Execute Brainf**k.',
            'args': [
                {
                    'name': 'input',
                    'help': 'Set the input.',
                    'keyvalue': '',
                    'optional': True,
                    },
                {
                    'name': 'code/input',
                    'help': 'Code to execute or input to set. ' +
                    'Use ! in the code to start input.',
                    'optional': False,
                    'end': True,
                    },
                ]
            })
    return m


maxloop = 500000


def evaluate(code, intextp):
    intext = intextp
    code = list(cleanup(list(code)))
    bracemap = buildbracemap(code)
    cells, codeptr, cellptr, outputlist = [0], 0, 0, []
    timesrun = 0

    while codeptr < len(code):
        timesrun += 1
        if timesrun > maxloop:
            return 'Max loop, Output: ' + ''.join(outputlist)
        command = code[codeptr]

        if command == ">":
            cellptr += 1
            if cellptr == len(cells):
                cells.append(0)

        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1

        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

        if command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]
        if command == ".":
            try:
                outputlist.append(chr(cells[cellptr]))
                if len(outputlist) > 250:
                    break
            except ValueError:
                pass
        if command == ",":
            try:
                cells[cellptr] = ord(intext[0])
                intext = intext[1:]
            except IndexError:
                cells[cellptr] = 0

        codeptr += 1
    return 'Output: ' + ''.join(outputlist)


def cleanup(code):
  return filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code)


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[":
            temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap


def bf(fp, args):
    if 'input' in args.lin:
        fp.server.state['bf.input'] = args.getlinstr('code/input')
        return 'Input is now "%s"' % args.getlinstr('code/input')
    else:
        try:
            fp.server.state['bf.input'] = args.getlinstr(
                'code/input').split('!')[1]
        except IndexError:
            pass
        return evaluate(args.getlinstr('code/input').split('!')[0],
            fp.server.state['bf.input'])