#!/usr/bin/env python


mport qiime2 as q2
from biom import Table
bt = q2.Artifact.load('deblur-ag/table.qza').view(Table)

with open('deblur-ag/representative-sequences.fna', 'w') as f:
    for i in bt.ids('observation'):
        f.write('>%s\n' % i)
        f.write('%s\n' % i)