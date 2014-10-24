#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getpid, getpgid, killpg, _exit, fork
from sys import exit
from signal import signal, SIGINT, SIGTERM, SIG_IGN
from time import sleep

def broadcast_to_proc_group(signum, frame):

    pid = getpid()
    pgid = getpgid(0)
    proc_is_parent = (pid == pgid)

    print '{} {} got {}, broadcast the signal and exit {}.'.format(
        'parent' if proc_is_parent else 'child',
        pid,
        signum,
        'gracefully' if proc_is_parent else 'immediately'
    )

    signal(signum, SIG_IGN)
    killpg(pgid, signum)

    if proc_is_parent:
        exit(signum)
    else:
        _exit(signum)

def main():

    signal(SIGINT, broadcast_to_proc_group)
    signal(SIGTERM, broadcast_to_proc_group)

    cpid = fork()

    print "I'm {}. I forked {}.".format(getpid(), cpid)

    while 1:
        print "I'm {}. I'm alive.".format(getpid())
        sleep(1)

if __name__ == '__main__':
    main()

