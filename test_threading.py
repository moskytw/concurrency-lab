#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import strftime, sleep
from threading import Lock, Thread, current_thread
from collections import deque

_log_lock = Lock()

def log(s):
    with _log_lock:
        print '[{}] [{}] {}'.format(
            strftime('%Y-%m-%d %H:%M:%S'),
            current_thread().name,
            s
        )

class WaitingQueue(object):

    def __init__(self, iterable):

        # only single thread can access its attrs at the same time
        self._lock = Lock()

        # the task queue
        self._q = deque(iterable)

        # if `take` when `_q` is empty, wait it or raise IndexError
        self._waiting = True

        # yeah, it's the condition mechanism, better than the built-in one
        self._wait_lock_q = deque()

    def put(self, x):

        with self._lock:

            # simply append it
            self._q.append(x)

            # notify a waiting take-thread
            try:
                wait_lock = self._wait_lock_q.popleft()
            except IndexError:
                pass
            else:
                wait_lock.release()

    def take(self):

        with self._lock:

            # pop
            # case 1: simply return it
            # case 2: wait for a `put`
            # case 3: raise IndexError

            try:
                return self._q.popleft()
            except IndexError:
                if not self._waiting:
                    raise

            # create an unique wait lock
            wait_lock = Lock()
            wait_lock.acquire()
            self._wait_lock_q.append(wait_lock)

        # acquire it secondly to wait and be notified
        wait_lock.acquire()
        return self.take()

    def stop_waiting(self):

        with self._lock:

            # let the futher take-thread raise
            self._waiting = False

            # notify all waiting take-threads
            while self._wait_lock_q:
                wait_lock = self._wait_lock_q.popleft()
                wait_lock.release()

if __name__ == '__main__':

    def consume():

        while 1:

            # try to take
            log('Trying to take ...')
            try:
                x = q.take()
            except IndexError:
                log('Failed to take. Stop.'.format(x))
                return
            else:
                log('Took {}.'.format(x))

            # consume
            log('Consuming {}...'.format(x))
            sleep(0.1)
            log('Consumed {}.'.format(x))

    q = WaitingQueue(range(4))
    for t in [Thread(target=consume) for i in range(3)]:
        t.start()

    # test to add tasks asyncly
    for x in 'ABC':
        log('Producing {}...'.format(x))
        q.put(x)
        log('Produced {}.'.format(x))

    # test to add tasks after queue empties
    sleep(0.8)
    for x in 'MNOP':
        log('Producing {}...'.format(x))
        q.put(x)
        log('Produced {}.'.format(x))

    # test to add tasks after stop waiting
    q.stop_waiting()
    sleep(0.5)
    for x in 'ST':
        log('Producing {}...'.format(x))
        q.put(x)
        log('Produced {}.'.format(x))

    log('End of Main.')

