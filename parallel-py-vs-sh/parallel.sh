#!/bin/bash

seq 0 9 | xargs -P10 -I{} ./do_task.sh {}
