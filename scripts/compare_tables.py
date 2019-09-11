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



cleaned_otus = 0
for index, row in rawOtuTable.iterrows():
    #print('<<<{}>>> {}'.format(index, row))
    cleaned_cells = 0
    cleaned_row = denoisedTable.loc[index, :]
    diff = row - cleaned_row
    for i, value in row.items():
        if cleaned_row[i] != value:
            cleaned_cells += 1

    if cleaned_cells > 0:
        print('{}\t{}\t{}'.format(index, cleaned_cells, row.max()))