#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randrange
from multiprocessing import Pool

def f(x):
    if randrange(3) == 0:
        raise RuntimeError('whatever')
    return x

if __name__ == '__main__':

    pool = Pool(3)

    items = range(10)
    results = [pool.apply_async(f, (item, )) for item in items]
    for item, result in zip(items, results):
        print item, result, result.get()

