#!/usr/bin/env python
# coding: utf-8

import sys
import numpy
import pandas
import argparse
import pdb
from pprint import pprint 

def eprint(*args, **kwargs):
    """print to STDERR"""
    print(*args, file=sys.stderr, **kwargs)


def verbose(message):
    """Print a verbose message (if --verbose is enabled)"""
    if opt.verbose:
        eprint(message)

if __name__ == '__main__':

    opt_parser = argparse.ArgumentParser(description='Normalize feature table')

    opt_parser.add_argument('-i', '--input',
                            help='OTU table filename',
                            required=True)
    opt_parser.add_argument('-o', '--output',
                            help='Output OTU table filename')
    opt_parser.add_argument('-s', '--separator',
                            help='feature table separator (default: \\t)',
                            default='\t')
                      
    opt_parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='Enable verbose output')

    opt = opt_parser.parse_args()

    # Import OTU table in "Qiime Classic format"
    try:
        data = pandas.read_csv(opt.input, sep=opt.separator, header=0, index_col=0)
    except Exception as e:
        eprint("FATAL ERROR: Unable to open {}. {}".format(opt.input, e))
        exit(1)

    verbose(f"Samples: {data.shape[0]}, Features (OTUs): {data.shape[1]}")

    # Select otus with sum > 100
    #  - Sum of each OTU: data.sum(axis=1)
    data.loc[data.sum(axis=1) > 100]
    data.loc[:, data.sum(axis=0) > 100]

    # Select OTUs having Y values > Z
    data.loc[(data > 100).sum(axis=1) > 5]
    
    # Select samples with sum > 10000
    data.loc[:, data.sum(axis=0) > 10000] 

    
    
    # Divide by the total counts of each sample
    normalized = data.divide(data.sum(axis=0))

    # Sort by OTU sum (row)
    # COL name -> df.sort_values('COL')
    normalized.loc[normalized.sum(axis=1).sort_values(ascending=False).index]

    # Check for duplicated index keys
    # normalized.index.duplicated().sum()
    
    # Round to integer (no missing allowed)
    # df.round(0).astype(int)

    normalized.to_csv(opt.input + '.norm' if opt.output is None else opt.output, sep='\t')
    #pdb.set_trace()
