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
        self._waiting = True

    def put(self, x):

        with self._lock:

            self._q.append(x)

            try:
                wait_lock = self._wait_lock_q.popleft()
            except IndexError:
                pass
            else:
                # notify the waiting take
                wait_lock.acquire(0)
                wait_lock.release()

    def take(self):

        with self._lock:

            try:
                return self._q.popleft()
            except IndexError:
                if not self._waiting:
                    raise

            # create an unique wait lock
            wait_lock = Lock()
            wait_lock.acquire() # lock it
            self._wait_lock_q.append(wait_lock)

        # wait to be notify
        wait_lock.acquire()
        return self.take()

    def stop_waiting(self):

        with self._lock:

            self._waiting = False

            for wait_lock in self._wait_lock_q:
                wait_lock.acquire(0)
                wait_lock.release()

if __name__ == '__main__':

    def consume():

        while 1:

            # try to take
            try:
                x = q.take()
            except IndexError:
                log('Got nothing.'.format(x))
                return

            # consume
            log('Consuming {}...'.format(x))
            sleep(0.1)
            log('Consumed {}.'.format(x))

    q = WaitingQueue(range(4))
    for t in [Thread(target=consume) for i in range(3)]:
        t.start()

    # test to add tasks asyncly
    for x in 'ABC':
        q.put(x)
        log('Put {} into queue.'.format(x))

    # test to add tasks after queue empties
    sleep(0.8)
    for x in 'MNOP':
        q.put(x)
        log('Put {} into queue.'.format(x))

    # test to add tasks after stop waiting
    q.stop_waiting()
    sleep(0.5)
    for x in 'ST':
        q.put(x)
        log('Put {} into queue.'.format(x))

    log('End of Main.')

