# -*- coding: utf-8 -*-


def remove_indices(l, indices):
    result = []
    i = 0
    for j in sorted(indices):
        result += l[i:j]
        i = j + 1
    result += l[i:]
    return result