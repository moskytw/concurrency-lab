#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from multiprocessing import Pool

def do_task(no):
    print 'Task {}: {:.9f}'.format(no, time())

processes_n = 10
pool = Pool(processes_n)

def parallelize(f, tasks_n):
    return pool.map(f, range(tasks_n))

if __name__ == '__main__':
    parallelize(do_task, processes_n)
