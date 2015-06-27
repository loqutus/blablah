#!/usr/bin/env python

import sys

def freq(FILENAME, OUTNAME):
    dict = {}
    with open(FILENAME) as f:
        for i in f.read():
            if i.isalpha():
                i = i.lower()
                if i in dict:
                    dict[i] = dict[i] + 1
                else:
                    dict[i] = 0
    with open(OUTNAME, 'w+') as f:
        for i in sorted(sorted(dict), key=dict.get, reverse=True):
            f.write(str(i) + ' ' + str(dict[i]) + '\n')

if __name__ == "__main__":
    FILENAME = sys.argv[1]
    OUTNAME = sys.argv[2]
    freq(FILENAME, OUTNAME)
    exit (0)
