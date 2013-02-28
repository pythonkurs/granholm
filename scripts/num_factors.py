#!/usr/bin/env python

import sys
from collections import Counter
import multiprocessing as mp
from IPython.parallel import Client

def factorize(n):
    if n < 2:
        return []
    factors = []
    p = 2

    while True:
        if n == 1:
            return factors
        r = n % p
        if r == 0:
            factors.append(p)
            n = n / p
        elif p * p >= n:
            factors.append(n)
            return factors
        elif p > 2:
            p += 2
        else:
            p += 1

def serial_factorization(LOW_NUM, HIGH_NUM):
    '''Factorize the numbers on one cpu serially'''
    num_unique_factors = []
    for n in xrange(LOW_NUM, HIGH_NUM):
       factors = factorize(n)
       num_unique_factors.append(len(factors))
    return Counter(num_unique_factors)

def multiproc_factorization(LOW_NUM, HIGH_NUM):
    '''Use multiprocessing Pool to factorize the numbers'''
    num_cpus = mp.cpu_count()
    pool = mp.Pool(processes=num_cpus-1)
    all_factors = pool.map(factorize, xrange(LOW_NUM, HIGH_NUM))
    num_unique_factors = []
    for factors in all_factors:
        num_unique_factors.append(len(factors))
    return Counter(num_unique_factors)

def ipython_factorization(LOW_NUM, HIGH_NUM):
    '''Parallelize using ipython'''
    try:
        client = Client()
        direct_view = client[:]

        @direct_view.parallel(block=True)
        def factorize(n):
            if n < 2:
                return []
            factors = []
            p = 2
        
            while True:
                if n == 1:
                    return factors
                r = n % p
                if r == 0:
                    factors.append(p)
                    n = n / p
                elif p * p >= n:
                    factors.append(n)
                    return factors
                elif p > 2:
                    p += 2
                else:
                    p += 1

        num_unique_factors = []
        all_factors = factorize.map(xrange(LOW_NUM, HIGH_NUM))
        for factors in all_factors:
            num_unique_factors.append(len(factors))
        return Counter(num_unique_factors)
    except IOError:
        sys.exit("IOError: Make sure to run 'ipcluster start -n 4' first")

def main():
    '''Factorize an integer either serially or parallel'''
    LOW_NUM = 2
    HIGH_NUM = 500000
    if sys.argv[1] == 's':
        # Serialize
        counts = serial_factorization(LOW_NUM, HIGH_NUM)
    elif sys.argv[1] == 'm':
        # Parallelize with multiprocessing
        counts = multiproc_factorization(LOW_NUM, HIGH_NUM)
    elif sys.argv[1] == 'i':
        # Parallelize with IPython.parallel
        counts = ipython_factorization(LOW_NUM, HIGH_NUM)
    print dict(counts)

if __name__ == '__main__':
    main()

