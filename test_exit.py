#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import atexit

def print_at_exit():
    print 'at exit.'

def main():

    atexit.register(print_at_exit)

    try:
        print 'in try.'
        sys.exit()
    except SystemExit:
        print 'in except SystemExit.'
    finally:
        print 'in finally.'

if __name__ == '__main__':

    main()
