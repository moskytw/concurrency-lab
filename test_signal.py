#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit
from os import getpid, fork, _exit
from time import sleep
from signal import signal, SIGINT, SIGKILL, SIGTERM, SIG_DFL

cpid = None

def print_n_exit(signum, frame):

    print "I'm {}. I just caught {}. I am leaving ...".format(getpid(), signum)

    cpid = frame.f_globals['cpid']
    if cpid is None or cpid != 0:
        exit(signum)
    else:
        _exit(signum)

signal(SIGINT, print_n_exit)
# can't be caught
#signal(SIGKILL, print_signal)
signal(SIGTERM, print_n_exit)

def main():

    global cpid

    cpid = fork()

    print "I'm {}. I forked {}.".format(getpid(), cpid)

    while 1:
        print "I'm {}. I'm alive.".format(getpid())
        sleep(1)

if __name__ == '__main__':
    main()

