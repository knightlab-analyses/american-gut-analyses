#!/usr/bin/env python
import qiime2 as q2
from biom import load_table, Table

bt = q2.Artifact.load('deblur-fmt-and-icu/table.qza').view(Table)

blooms = []
with open('newbloom.all.fna', 'r') as f:
    for line in f.read().split('\n'):
        if line.startswith('>'):
            pass
        else:
            blooms.append(line.strip())
blooms = [b[:125] for b in blooms]
to_remove = set(bt.ids('observation')) & set(blooms)

bt.filter(to_remove, axis='observation', invert=True, inplace=True)
q2.Artifact.import_data("FeatureTable[Frequency]", bt).save('deblur-fmt-and-icu/table.noblooms.qza')


# bt = q2.Artifact.load('deblur-fmt-and-icu/table.noblooms.qza').view(Table)
with open('deblur-fmt-and-icu/representative-sequences.fna', 'w') as f:
    for i in bt.ids('observation'):
        f.write('>%s\n' % i)
        f.write('%s\n' % i)