import click
import skbio
import pandas as pd


@click.command()
@click.option('--input', type=click.Path(exists=True), required=True)
@click.option('--output', type=click.Path(exists=False), required=True)
@click.option('--mapping', type=click.Path(exists=True), required=True)
def subset(input, output, mapping):
    md = pd.read_csv(mapping, sep='\t', dtype=str).set_index('#SampleID')

    dm = skbio.DistanceMatrix.read(input)
    dm.ids = tuple(['x%s' % i for i in dm.ids])

    dm_filt = dm.filter(md.index, strict=False)
    dm_filt.write(output)


if __name__ == '__main__':
    subset()
