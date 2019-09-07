#!/usr/bin/env python

import pandas
import argparse
import sys
import pdb


def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)


def vprint(msg):
    if opt.verbose:
        eprint('# {}'.format(msg))


opt_parser = argparse.ArgumentParser(description='"samtools depth" to bed')

opt_parser.add_argument('-t', '--otutable',
                        help='Input OTU table',
                        required=True)
opt_parser.add_argument('-d', '--denoisedtable',
                        type=argparse.FileType('r'),
                        help='Output (denoised) OTU table',
                        required=True)

opt_parser.add_argument('-k', '--key',
                        help='OTU ID in the OTU table [#OTU ID]',
                        default='#OTU ID')

opt_parser.add_argument('-v', '--verbose',
                        help='Increase output verbosity',
                        action='store_true')

opt = opt_parser.parse_args()

denoisedTable = pandas.read_csv(opt.denoisedtable, sep='\t',index_col=0)

rawOtuTable = pandas.read_csv(opt.otutable, sep='\t', index_col=0)



for index, row in rawOtuTable.iterrows():
    #print('<<<{}>>> {}'.format(index, row))
    xrow = denoisedTable.loc[index, :]
    diff = row - xrow
    print(row, xrow)