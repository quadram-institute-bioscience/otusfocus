#!/usr/bin/env python
# coding: utf-8

# Example command:
# python3 /local/giovanni/otusfocus/scripts/denoise_dev_function.py -i /local/giovanni/otusfocus/otu_tables/example3/otutab.tsv
# /local/giovanni/otusfocus/scripts/denoise_dev_function.py -i /local/giovanni/otusfocus/otu_tables/example3/otutab.tsv

import sys
import numpy
import pandas
import argparse
from scipy.optimize import minimize

# Program defaults
from typing import Any

def denoiseTable(data, threshold_ratio = 0.04, min_low_samples = 3, min_sample_ratio = 0.15, min_otu_counts  = 1000, min_candidates  = 9, max_cross_index = 0.01):
    """
    Denoise an OTU table
    Parameters: OTU Table, threshold_ratio = 0.1, min_low_samples = 3, min_sample_ratio = 0.15, min_otu_counts  = 1000, min_candidates  = 10, max_cross_index     = 0.02
    Output: Cleaned OTU table
    """
    numOtus, numSamples = data.shape

    verbose(' - Total OTUs: {}\n - Total samples: {}'.format(numOtus, numSamples))

    if numSamples * min_sample_ratio > min_low_samples:
        min_low_samples = int(numSamples * min_sample_ratio)
        verbose(' - Min cross talk samples: {}'.format(min_low_samples))

    verbose(' - Scanning OTU table to estimate cross talk index')

    otu_means = data.mean(axis=1)
    low_cells = (0 < data) & data.le(threshold_ratio * otu_means, axis=0)
    num_samples_low = low_cells.sum(axis=1)
    tot_samples_low = (data * low_cells).sum(axis=1)
    row_tot = data.sum(axis=1)

    cross_index = (tot_samples_low / row_tot) * (numSamples / tot_samples_low)
    candidates = (tot_samples_low > min_low_samples) & (row_tot > min_otu_counts) & (cross_index <= max_cross_index)
    if candidates.sum() < min_candidates:
        verbose('Not enough OTU candidates to estimate cross talk')
        return data

    cross_talk_median = cross_index.loc[candidates].median()

    verbose('Median cross talk: {}'.format(cross_talk_median))

    #all counts ≤ z(i) are crosstalk: set them to zero
    Zi = cross_talk_median * row_tot / data.shape[1]

    # 't' series

    dividedData = data.divide(Zi, axis=0)
    t = 2 / (1 + numpy.exp(dividedData.clip(upper=100)))


    #if False:
    #    t = 0
    #    if data.divide(Zi, axis=0) < 100:
    #        t = 2 / (1 + numpy.exp(data.divide(Zi, axis=0)))

    denoised_data = data.where(t < threshold_ratio, 0)

    #from IPython import embed
    #embed()
    #assert False
    data.loc[(data - denoised_data > 0).any(axis=1)]
    
    if opt.output is None:
        opt.output = opt.input + '.cleaned'

    return denoised_data


def compareTables(firstTable,secondTable):
    """Compare two data frames and return the sum of squares of the differences"""
    deltaTable = firstTable - secondTable
    return deltaTable.abs().sum().sum() * (deltaTable != 0).sum().sum()

def denoiseTableWithReference(x):
    """Receive a vector of parameters (threshold_ratio = 0.1, min_low_samples = 3, min_sample_ratio = 0.15, max_cross_index = 0.02)
    and return a cleaned matrix"""
    #threshold_ratio = 0.1, min_low_samples = 3, min_sample_ratio = 0.15, max_cross_index = 0.02
    cleanedTable = denoiseTable(data, threshold_ratio=x[0], min_low_samples=int(x[1]), min_sample_ratio=x[2], max_cross_index=x[3])
    return compareTables(cleanedTable,referenceTable)


def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)


def verbose(message):
    """Print a verbose message (if --verbose is enabled)"""
    if opt.verbose:
        eprint(message)

def debug(message):
    """Print a debug message prepending # (requires  --debug enabled)"""
    if opt.debug:
        eprint('#{}'.format(message))



if __name__ == '__main__':

    opt_parser = argparse.ArgumentParser(description='Denoise Illumina cross-talk from OTU tables')

    opt_parser.add_argument('-i', '--input',
                            help='OTU table filename',
                            required=True)

    opt_parser.add_argument('-r', '--reference',
                            help='Reference cleaned OTU table filename'
                            )

    opt_parser.add_argument('-o', '--output',
                            help='Cleaned OTU table filename',
                            )
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

    if opt.reference != None:
        referenceTable = pandas.read_csv(opt.reference, sep='\t', header=0, index_col=0)
        x0 = numpy.array([0.1, 3, 0.15, 0.02])
        bounds = ([0, 2], [1.0, 6.0], [0.05, 0.3], [0.01, 0.05])
        #res = minimize(denoiseTableWithReference, x0, method='COBYLA', bounds=bounds,options={ 'disp': True})
        #print(res)
        c=0
        min=None
        max=None
        for threshold in numpy.arange(0, 2, 0.1):
            for lowsamples in numpy.arange(1.0, 5.0, 0.5):
                for min_sample_ratio in numpy.arange(0.01, 0.30, 0.025):
                    for max_cross_index in numpy.arange(0.1, 0.5, 0.05):
                        c += 1
                        x = numpy.array([threshold, lowsamples, min_sample_ratio, max_cross_index])
                        r = denoiseTableWithReference(x)
                        if min == None:
                            min = r
                            max = r
                            print('*{} {}: thr={} lowsamples={} minsampleratio={} maxcross={}'.format(c, r, threshold,
                                                                                                     lowsamples,
                                                                                                     min_sample_ratio,
                                                                                                     max_cross_index))

                        if min > r:
                            min = r
                            print('<{} {}: thr={} lowsamples={} minsampleratio={} maxcross={}'.format(c, r, threshold,
                                                                                                     lowsamples,
                                                                                                     min_sample_ratio,
                                                                                                     max_cross_index))

                        if max < r:
                            max = r
                            print('>{} {}: thr={} lowsamples={} minsampleratio={} maxcross={}'.format(c, r, threshold,
                                                                                                      lowsamples,
                                                                                                      min_sample_ratio,
                                                                                                      max_cross_index))









    else:
        cleanedTable = denoiseTable(data)
        cleanedTable.to_csv(opt.input + '.cleaned' if opt.output is None else opt.output, sep='\t')

    exit()
