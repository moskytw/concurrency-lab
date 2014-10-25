#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getpid, getpgid
from time import sleep

# bash -c "echo $$; ./print_pid.py; ./print_pid.py"
# pstree <pid>
# pgrep <pid>
# pkill <pid>

print 'pid : {}'.format(getpid())
print 'pgid: {}'.format(getpgid(0))
print 'go sleep ...'
sleep(100)
