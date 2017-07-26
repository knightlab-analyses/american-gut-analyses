import skbio.diversity
import sys
import biom
import pandas as pd

table = biom.load_table(sys.argv[1])
tree = skbio.TreeNode.read(sys.argv[2])
md = pd.read_csv(sys.argv[3], sep='\t', dtype=str).set_index('#SampleID')

tree_names = {tree.name(i) for i in range(tree.B.size) if tree.B[i] if tree.name(i) is not None and tree.name(i)[0] in 'ATGC'}
tree_names = {n.name for n in range(tree.tips()) n.name[0] in 'ATGC'}
table_names = set(table.ids(axis='observation'))

tree = tree.shear(set(table.ids(axis='observation')))
ids = table.ids(axis='observation')

faith = pd.Series([])
shannon = pd.Series([])
observed = pd.Series([])
for v, i, _ in table.iter(dense=True):
    r = skbio.diversity.alpha_diversity('faith_pd', (v > 0), otu_ids=ids, tree=tree, validate=True)
    r.index = [i]
    faith = faith.append(r)

    r = skbio.diversity.alpha_diversity('shannon', (v > 0), validate=True)
    r.index = [i]
    shannon = shannon.append(r)

    r = skbio.diversity.alpha_diversity('observed_otus', (v > 0), validate=True)
    r.index = [i]
    observed = observed.append(r)

faith.name = 'faith_pd'
shannon.name = 'shannon'
observed.name = 'observed'
md = md.join(faith)
md = md.join(shannon)
md = md.join(observed)
md.to_csv(sys.argv[1] + '.adiv.txt', sep='\t', index=True, header=True)
