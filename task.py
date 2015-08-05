#!/usr/bin/env python

import sys


def freq(filename, outname):
    res = {}
    with open(filename) as f:
        for j in f:
            for i in j:
                if i.isalpha():
                    i = i.lower()
                    if i in res:
                        res[i] += 1
                    else:
                        res[i] = 1

    with open(outname, 'w+') as f:
        for i in sorted(sorted(res), key=res.get, reverse=True):
            f.write(str(i) + ' ' + str(res[i]) + '\n')


if __name__ == "__main__":
    FILENAME = sys.argv[1]
    OUTNAME = sys.argv[2]
    freq(FILENAME, OUTNAME)
    exit(0)
