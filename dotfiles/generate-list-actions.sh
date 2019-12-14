#!/bin/sh
echo "Methods:"
grep " def " actions.py | sed -e 's/ def //' | sed -e 's/self//' | sed -e 's/(, /(/' | sed -e 's/()//' | sort -n

echo "Dynamic routes:"
grep "r\"" actions.py | grep "\["
