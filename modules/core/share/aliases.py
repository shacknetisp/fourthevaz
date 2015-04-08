# -*- coding: utf-8 -*-
aliases = {
    'give': 'echo $#: <*$*>',
    'kickban':
        'absorb "Attempted to kickban $1" <kick $1 $*><ban $1>',
    'nand': 'not <and $# $#>',
    'nor': 'not <or $# $#>',
    'xor': 'not <eq <not $#> <not $#>>'
    }