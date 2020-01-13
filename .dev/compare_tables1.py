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

opt_parser.add_argument('otutable',
                        help='Input OTU table',
                        )
opt_parser.add_argument('denoisedtable',
                        type=argparse.FileType('r'),
                        help='Output (denoised) OTU table',
                        )

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
deltaTable = denoisedTable - rawOtuTable

(deltaTable != 0)
assert False

rawOtuTable.max(axis=1)


row_index = 0
for index, row in rawOtuTable.iterrows():
    row_index += 1
    vprint('<<<{}>>> {}'.format(index, row))
    cleaned_cells = 0
    cleaned_row = denoisedTable.loc[index, :]
    diff = row - cleaned_row
    for i, value in row.items():
        if cleaned_row[i] != value:
            cleaned_cells += 1

    if cleaned_cells > 0:
        print('{}|{}\tdenoised_cells={}\tmax={}'.format(row_index,index, cleaned_cells, row.max()))
