import sys
import biom
import h5py
import pandas as pd


ta = biom.load_table(sys.argv[1])
tb = biom.load_table(sys.argv[2])
md = pd.read_csv(sys.argv[3], sep='\t', dtype=str).set_index('#SampleID')

ids = {l.strip() for l in open('abx.ids')}
ta_abx = ta.filter(lambda v, i, _: i in ids, inplace=False).remove_empty()
tb_abx = tb.filter(lambda v, i, _: i in ids, inplace=False).remove_empty()

# sample so extremes are balanced

assert set(ta_abx.ids()) == set(tb_abx.ids())

mdabx = md.loc[ta_abx.ids()]
abx_week_ids = set(mdabx[mdabx['ANTIBIOTIC_HISTORY'] == 'Week'].index)
abx_year_ids = set(mdabx[mdabx['ANTIBIOTIC_HISTORY'] == 'I have not taken antibiotics in the past year.'].sample(len(abx_week_ids)).index)
ta_abx_low = ta_abx.filter(lambda v, i, m: i in abx_week_ids, inplace=False).remove_empty()
ta_abx_high = ta_abx.filter(lambda v, i, m: i in abx_year_ids, inplace=False).remove_empty()
tb_abx_low = tb_abx.filter(lambda v, i, m: i in abx_week_ids, inplace=False).remove_empty()
tb_abx_high = tb_abx.filter(lambda v, i, m: i in abx_year_ids, inplace=False).remove_empty()


with h5py.File(sys.argv[1] + '.abx-low.biom', 'w') as fp:
    ta_abx_low.to_hdf5(fp, 'asd')
with h5py.File(sys.argv[1] + '.abx-high.biom', 'w') as fp:
    ta_abx_high.to_hdf5(fp, 'asd')

with h5py.File(sys.argv[2] + '.abx-low.biom', 'w') as fp:
    tb_abx_low.to_hdf5(fp, 'asd')
with h5py.File(sys.argv[2] + '.abx-high.biom', 'w') as fp:
    tb_abx_high.to_hdf5(fp, 'asd')
