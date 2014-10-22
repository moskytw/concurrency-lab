#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit
from os import getpid, fork
from time import sleep
from signal import signal, SIGINT, SIGKILL, SIGTERM

def print_signal(signum, frame):
    print "I'm {}. I just caught {}. I am leaving.".format(getpid(), signum)
    exit()

signal(SIGINT, print_signal)
# can't be caught
#signal(SIGKILL, print_signal)
signal(SIGTERM, print_signal)

if __name__ == '__main__':

    cpid = fork()
    print "I'm {}. I forked {}.".format(getpid(), cpid)

    while 1:
        print "I'm {}. I'm alive.".format(getpid())
        sleep(1)
