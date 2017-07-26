import bp
import skbio.diversity
import skbio.stats
import biom
import click


@click.command()
@click.option('-i', type=click.Path(exists=True))
@click.option('-t', type=click.Path(exists=True))
@click.option('-m', type=str)
@click.option('-o', type=click.Path(exists=False))
def unif(table, tree, method, output):
    table = biom.load_table(tree)
    ids = table.ids()
    otu_ids = table.ids(axis='observation')
    mat = table.matrix_data.T.astype(int).toarray()

    tree = bp.parse_newick(open(tree).read())
    tree = tree.shear(set(otu_ids)).collapse()
    tree = bp.to_skbio_treenode(tree)

    dm = skbio.diversity.beta_diversity(method, mat, ids=ids, otu_ids=otu_ids, tree=tree)
    pc = skbio.stats.ordination.pcoa(dm)

    pc.write(output)


if __name__ == '__main__':
    unif()
