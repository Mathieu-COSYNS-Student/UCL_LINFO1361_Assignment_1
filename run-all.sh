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

FILES=(
    'instances/a01'
)

for i in "${FILES[@]}"; do
    echo "-----------------------------------------"
    echo "$i"
    echo "-----------------------------------------"
    timeout 45s python rubik2D.py "$i" || echo "Timeout"
    echo "-----------------------------------------"
    echo ""
done