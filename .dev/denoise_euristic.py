#!/usr/bin/env python
# coding: utf-8
# ipython -i ./denoise_giovanni_euristic.py -- ../otu_tables/example1/otutab.tsv -o ../otu_tables/example1/otutab.gioclean.tsv

import sys
import numpy
import pandas
import argparse
import statistics
import math
from scipy.linalg import inv

# Program defaults
from typing import Any

threshold_ratio = 0.1
min_low_samples = 3
min_sample_ratio = 0.15
min_otu_counts  = 1000
min_candidates  = 10
max_cross_index = 0.02


def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)


def verbose(message):
    if opt.verbose:
        eprint(message)

def debug(message):
    if opt.debug:
        eprint('#{}'.format(message))

opt_parser = argparse.ArgumentParser(description='Denoise Illumina cross-talk from OTU tables')

opt_parser.add_argument('input',
                        help='OTU table filename', nargs='?')

opt_parser.add_argument('-o', '--output',
                        help='Cleaned OTU table filename',
                        )
opt_parser.add_argument('-v', '--verbose',
                        help='Print extra information',
                        action='store_true')

opt_parser.add_argument('-m', '--method',
                        default='L-BFGS-B',
                        help='Optimization method')

opt_parser.add_argument('-d', '--debug',
                        help='Print debug information',
                        action='store_true')



opt = opt_parser.parse_args()


import numpy
from scipy.optimize import minimize

from numba import jit

import cProfile

@jit(nopython=True)
def vector2cross_talk_matrix(x, n):
    ct = numpy.zeros((n, n))
    l = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                 ct[i, j] = x[l]
                 l += 1
        ct[i,i] = 1 - numpy.sum(ct[i])
    return ct

if opt.input is None:
    eprint('TEST MODE')
    n = 16
    print('Samples:', n)
    clean_count_test = numpy.concatenate([numpy.identity(n)*(10**i) for i in range(1, 3)])
    print('Clean counts:\n', clean_count_test)
    cross_talk_test = numpy.zeros(n*(n-1))
    cross_talk_test[2] = 0.01
    print('Cross talk:\n', vector2cross_talk_matrix(cross_talk_test, n))
    raw_count_test = numpy.dot(clean_count_test, vector2cross_talk_matrix(cross_talk_test, n))
    print('Raw counts:\n', raw_count_test)
    data = raw_count_test
else:
# Import OTU table in "Qiime Classic format"
    try:
        data = pandas.read_csv(opt.input, sep='\t', header=0, index_col=0)
    except Exception as e:
        eprint("FATAL ERROR: Unable to open {}. {}".format(opt.input, e))
        exit(1)


def euristic_loss(ct, ob, ct_reg_weight=1):
    ict = inv(ct)
    tc = numpy.dot(ob, ict)
    return numpy.sum(numpy.log(tc**2 + 0.01)) + ct_reg_weight*numpy.sum((1 - ct[numpy.diag_indices_from(ct)])**2)

def euristic_loss_inv(ict, ob, ct_reg_weight=10):
    tc = numpy.dot(ob, ict)
    return numpy.sum(numpy.log(tc**2 + 0.01)) + ct_reg_weight*numpy.sum((numpy.identity(ict.shape[1]) - ict)**2)


from numpy.random import rand

def find_clean_counts(raw_counts):
    n = raw_counts.shape[1]
    def func(x):
        return euristic_loss(vector2cross_talk_matrix(x, n), raw_counts)
    param_n = n*(n-1)
    x0 = rand(param_n)*0.05
    #x0 = [0.01 for _ in range(param_n)]
    bounds = [(0, 0.05) for _ in range(param_n)]
    res = minimize(func, x0=x0, bounds=bounds, options={'disp': True}, method=opt.method)
    estimed_cross_talk = vector2cross_talk_matrix(res.x, n)
    estimed_clean_counts = numpy.dot(raw_counts, inv(estimed_cross_talk))
    return estimed_clean_counts, estimed_cross_talk, res

def find_clean_counts_inv(raw_counts):
    n = raw_counts.shape[1]
    def func(x):
        return euristic_loss_inv(x.reshape(n, n), raw_counts)
    param_n = n*n
    x0 = rand(param_n)*0.05
    #x0 = [0.01 for _ in range(param_n)]
    bounds = [(0, 0.05) for _ in range(param_n)]
    res = minimize(func, x0=x0, bounds=bounds, options={'disp': True}, method=opt.method)
    estimed_cross_talk = inv(res.x.reshape(n, n))
    estimed_clean_counts = numpy.dot(raw_counts, inv(estimed_cross_talk))
    return estimed_clean_counts, estimed_cross_talk, res


#cProfile.run('find_clean_counts(data)')
#cProfile.run('find_clean_counts_inv(data)')

#assert False
xcc, xct, res = find_clean_counts(data)
eprint(res)
if opt.input is None:
    print('Extimated clean counts:\n', numpy.round(xcc, 1))
    print('Extimated cross talk:\n', numpy.round(xct, 4))
else:
    output_path = opt.input + '.cleaned' if opt.output is None else opt.output
    xcc.to_csv(output_path, sep='\t')
    xct.to_csv(output_path + '.cross_talk', sep='\t')
