#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import strftime, sleep
from threading import Lock, Thread
from collections import deque

_log_lock = Lock()

def log(s):
    with _log_lock:
        print '[{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S'), s)

class WaitingQueue(object):

    def __init__(self, iterable):

        self._lock = Lock()
        self._q = deque(iterable)
        # yeah, it's the condition mechanism
        self._wait_lock_q = deque()

    def put(self, x):

        with self._lock:

            self._q.append(x)

            try:
                wait_lock = self._wait_lock_q.popleft()
            except IndexError:
                pass
            else:
                # notify the waiting take
                wait_lock.release()

    def take(self):

        with self._lock:

            try:
                return self._q.popleft()
            except IndexError:
                pass

            # create an unique wait lock
            wait_lock = Lock()
            wait_lock.acquire() # lock it
            self._wait_lock_q.append(wait_lock)

        # wait to be notify
        with wait_lock:
            return self.take()

    def stop_waiting(self):

if __name__ == '__main__':

    q = WaitingQueue(range(10))

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

