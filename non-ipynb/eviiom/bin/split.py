import sys
import biom
import h5py

t = biom.load_table(sys.argv[1])
ids = {l.strip() for l in open('abx.ids')}
tabx = t.filter(lambda v, i, md: i in ids, inplace=False).remove_empty()

with h5py.File(sys.argv[1] + '.abx.biom', 'w') as fp:
    tabx.to_hdf5(fp, 'asd')
