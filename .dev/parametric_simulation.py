import numpy
import pandas

df = pandas.read_table('/local/giovanni/otusfocus/otu_tables/example1/otutab.tsv', index_col=0)
ct_index = df.median(axis=1) < df.max(axis=1)*0.05



n=20
# true counts
tc = numpy.concatenate((numpy.identity(n)*100,numpy.identity(n)*1000))
# cross talk matrix
ct = numpy.identity(n)
ct = numpy.identity(n) - 0.001

# observed counts
oc = numpy.dot(tc,ct)




def compute_observed_matrix(m, ct):
    pass

#loss = numpy.sum(numpy.log(df))

#def ct_candidate(
#df.apply(lambda r: r.nlargest(2), axis=1)

