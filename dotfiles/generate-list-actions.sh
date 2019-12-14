#!/bin/sh
grep " def " actions.py | sed -e 's/ def //' | sed -e 's/self//' | sed -e 's/(, /(/' | sed -e 's/()//' | sort -n
