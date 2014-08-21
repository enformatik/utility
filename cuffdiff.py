#!/usr/bin/env python
from optparse import OptionParser
import math

################################################################################
# cuffdiff.py
#
# Methods to aid analysis of cuffdiff output
################################################################################


################################################################################
# main
################################################################################
def main():
    usage = 'usage: %prog [options] arg'
    parser = OptionParser(usage)
    #parser.add_option()
    (options,args) = parser.parse_args()


################################################################################
# hash_diff
# 
# Input:
#  diff_file:     RIP *_exp.diff file.
#  stat:          test_stat or fold
#  max_stat:      Maximum abs value allowed for the diff stat.
#  min_fpkm:      Minimum FPKM to consider a gene.
#  sample_first:  Sample name to force to come first (e.g input/control/etc)
#
# Output:
#  gene_diff:     Dict mapping sample pairs to dicts mapping gene_id to diff stat
################################################################################
def hash_diff(diff_file, stat='fold', max_stat=None, min_fpkm=None, sample_first=None):
    gene_diff = {}

    # read rip diff
    diff_in = open(diff_file)
    diff_in.readline()
    for line in diff_in:
        a = line.split('\t')

        gene_id = a[0]
        sample1 = a[4]
        sample2 = a[5]
        status = a[6]
        fpkm1 = float(a[7])
        fpkm2 = float(a[8])
        fold_change = float(a[9])
        test_stat = float(a[10])
        qval = float(a[11])
        sig = a[-1].rstrip()

        if sample2 == force_first:
            sample2, sample1 = sample1, sample2
            fpkm2, fpkm1 = fpkm1, fpkm2
            fold_change *= -1
            test_stat *= -1

        if status == 'OK' and not math.isnan(test_stat):
            if min_fpkm == None or fpkm1 > min_fpkm or fpkm2 > min_fpkm:
                if stat in ['fold','fold_change']:
                    diff_stat = fold_change
                elif stat in ['test_stat','tstat']:
                    diff_stat = test_stat
                else:
                    print >> sys.stderr, 'Unknown stat requested: %s' % stat
                    exit(1)

                if max_stat != None:
                    diff_stat = min(diff_stat, abs(max_stat))
                    diff_stat = max(diff_stat, -abs(max_stat))

                gene_diff.setdefault((sample1,sample2),{})[gene_id] = diff_stat

    diff_in.close()

    return gene_diff


################################################################################
# hash_diff_one
# 
# Input:
#  diff_file:     RIP *_exp.diff file.
#  stat:          test_stat or fold
#  max_stat:      Maximum abs value allowed for the diff stat.
#  min_fpkm:      Minimum FPKM to consider a gene.
#  sample_first:  Sample name to force to come first (e.g input/control/etc)
#
# Output:
#  gene_diff:     Dict mapping gene_id to diff stat
################################################################################
def hash_diff_one(diff_file, stat='fold', max_stat=None, min_fpkm=None, sample_first=None):
    gene_diff = hash_diff(diff_file, stat, max_stat, min_fpkm, sample_first)
    if len(gene_diff.keys()) > 1:
        print >> sys.stderr, 'More than one pair of samples found in %s' % diff_file
        exit(1)
    else:
        samples = gene_diff.keys()[0]
        return gene_diff[samples]


################################################################################
# __main__
################################################################################
if __name__ == '__main__':
    main()