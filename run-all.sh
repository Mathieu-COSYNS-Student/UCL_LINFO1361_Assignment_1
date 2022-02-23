#!/bin/bash

FILES=(
    'instances/a01'
    'instances/a02'
    'instances/a03'
    'instances/a04'
    'instances/a05'
    'instances/b01'
    'instances/b02'
    'instances/b03'
    'instances/b04'
    'instances/b05'
)

# FILES=(
#    'instances/b05'
# )

for i in "${FILES[@]}"; do
    echo "-----------------------------------------"
    echo "$i"
    echo "-----------------------------------------"
    ulimit -v 3000000
    timeout 180s python rubik2D.py "$i" || echo "Timeout"
    echo "-----------------------------------------"
    echo ""
done
