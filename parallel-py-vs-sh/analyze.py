#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

def to_ms(ns):
    return ns/10.**6

# get nanoseconds
ns_re = re.compile('\d{9}')
nss = map(int, ns_re.findall(sys.stdin.read()))

# min & max
min_ns = min(nss)
max_ns = max(nss)

print 'min: {:.6f}'.format(to_ms(min_ns))
print 'max: {:.6f}'.format(to_ms(max_ns))
print 'max-min: {:.6f}'.format(to_ms(max_ns-min_ns))
