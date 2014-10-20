#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import strftime, sleep
from threading import Lock, Thread
from collections import deque

_log_lock = Lock()

def log(s):
    with _log_lock:
        print '[{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S'), s)

class BlockingQueue(object):

    def __init__(self, iterable):
        self._op_lock = Lock()
        self._q = deque(iterable)

    def put(self, x):
        with self._op_lock:
            self._q.append(x)

    def take(self):
        with self._op_lock:
            return self._q.popleft()

if __name__ == '__main__':

    q = BlockingQueue(range(10))

    def consume():

        while 1:
            x = q.take()
            log('Consuming {}...'.format(x))
            sleep(0.1)
            log('Consumed {}.'.format(x))

    for t in [Thread(target=consume) for i in range(3)]:
        t.start()

    sleep(0.1)
    for x in 'AB':
        q.put(x)
        log('Put {} into queue.'.format(x))

    sleep(2)
    for x in 'XY':
        q.put(x)
        log('Put {} into queue.'.format(x))

    log('End of Main')

