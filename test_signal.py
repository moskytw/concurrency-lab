#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit
from os import getpid, kill, fork, _exit
from time import sleep
from signal import signal, SIGINT, SIGKILL, SIGTERM, SIG_DFL

cpid = None

def do_fun_things(signum, frame):

    print "I'm {}. I just caught {}. I am leaving ...".format(getpid(), signum)

    cpid = frame.f_globals['cpid']
    if cpid is None:
        exit(signum)
    elif cpid != 0:
        # ctrl-c will send to both, but kill <pid> won't
        # use kill to relay signal
        kill(cpid, signum)
        exit(signum)
    else:
        _exit(signum)

signal(SIGINT, do_fun_things)
# can't be caught
#signal(SIGKILL, do_fun_things)
signal(SIGTERM, do_fun_things)

def main():

    global cpid

    cpid = fork()

    print "I'm {}. I forked {}.".format(getpid(), cpid)

    while 1:
        print "I'm {}. I'm alive.".format(getpid())
        sleep(1)

if __name__ == '__main__':
    main()

