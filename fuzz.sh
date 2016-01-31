#!/bin/sh
set -e
while true; do
    python3 fuzz.py > f.nim
    nim c --verbosity:0 f
done
