#!/usr/bin/env python3

from math import pi

def printmutitable():
    for i in range(1,10):
        for j in range(1,i+1):
            print('{}x{}={}'.format(j,i,i*j),end="\t")
        print('')

def circlearea(r):
    '''Caculate area for circle'''
    return (pi * int(r) ** 2)

def same_number(begin=80,end=74):
    if begin < end:
        begin , end = end, begin
    return (begin - end) / 2


if __name__ == '__main__':
    print(printmutitable())