#!/usr/bin/env python
# coding: utf-8

import sys
import pandas
import argparse
import statistics
import math
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

opt_parser.add_argument('-i', '--input',
                        help='OTU table filename',
                        required=True)

opt_parser.add_argument('-v', '--verbose',
                        help='Print extra information',
                        action='store_true')

opt_parser.add_argument('-d', '--debug',
                        help='Print debug information',
                        action='store_true')



opt = opt_parser.parse_args()

# Import OTU table in "Qiime Classic format"
try:
    data = pandas.read_csv(opt.input, sep='\t', header=0, index_col=0)
except Exception as e:
    eprint("FATAL ERROR: Unable to open {}. {}".format(opt.input, e))
    exit(1)

(tot_otus, tot_samples) = data.shape
verbose(' - Total OTUs: {}\n - Total samples: {}'.format(tot_otus, tot_samples))

if tot_samples * min_sample_ratio > min_low_samples:
    min_low_samples =  int(tot_samples * min_sample_ratio)
    verbose(' - Min cross talk samples: {}'.format( min_low_samples ))


candidates = 0
candidates_df = pandas.DataFrame(columns=data.columns)

cross_talk_indices = []

verbose(' - Scanning OTU table to estimate cross talk index')
for index, row in data.iterrows():

    otu_mean = row.mean()
    otu_max  = row.max()

    num_samples_low = 0
    tot_samples_low = 0
    for cell in row:
        if 0 < cell <= (threshold_ratio * otu_mean):
            num_samples_low += 1
            tot_samples_low += cell
    if tot_samples_low > min_low_samples and row.sum() > min_otu_counts:
        candidates += 1
        cross_index = (tot_samples_low / row.sum() ) * ( tot_samples / tot_samples_low )

        if cross_index <= max_cross_index:
            debug('CANDIDATE {}\ti={}\tmax={}\tmean={}\tsamples={}\tsumLow={}'.format(index, cross_index, otu_max, otu_mean, num_samples_low, tot_samples_low))
            cross_talk_indices.append(cross_index)




verbose('{}/{}\t{}% candidate otus'.format(candidates, tot_otus, round(candidates * 100/ tot_otus, 2)))

if len(cross_talk_indices) < min_candidates:
    eprint('Not enough OTU candidates to estimate cross talk')
    exit()


cross_talk_median = statistics.median(cross_talk_indices)
eprint('Median cross talk: {}'.format(cross_talk_median))
for index, row in data.iterrows():

    otu_mean = row.mean()
    otu_max = row.max()

    zero = cross_talk_median * (row.sum() / tot_samples)
    for value in row.values:
        pass
        #t_score = 2 / ( 1 + math.exp( value / zero ) )
        #debug('{}\t{}/{}'.format((value/zero), value, zero))
        #print('{}\t{}/{}'.format(math.exp(value / zero), value, zero))
    if zero > 1:
        pass
        #print('{}\t{}\t{}\tmax={} mean={}'.format(index, t_score, zero, otu_max, otu_mean))
        #debug(row.values)
