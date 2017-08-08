#!/bin/bash
set -ex

source activate qiime2-2017.4

# use high performance local disk to each node
export TMPDIR=/localscratch
tmp=$(mktemp -d --tmpdir)
export TMPDIR=$tmp

# from http://stackoverflow.com/a/2130323
function cleanup {
  echo "Removing $tmp"
  rm  -r $tmp
  unset TMPDIR
}
trap cleanup EXIT

cwd=$(pwd)
pushd $tmp

curl -o raw-sequences.fna.gz ftp://ftp.microbio.me/pub/publications-files/american-gut/raw-sequences.fna.gz

curl -L -o gg-13-8-99-515-806-nb-classifier.qza https://data.qiime2.org/2017.4/common/gg-13-8-99-515-806-nb-classifier.qza
curl -L -o expand.py https://raw.githubusercontent.com/wasade/reimagined-fiesta/master/expand.py
curl -L -o sepp-package.tar.bz https://raw.github.com/smirarab/sepp-refs/master/gg/sepp-package.tar.bz
tar xfj sepp-package.tar.bz
pushd sepp-package/sepp
python setup.py config -c
popd

zcat $HOME/raw-sequences.fna.gz > raw-sequences.fna
deblur workflow --seqs-fp raw-sequences.fna --output-dir ag-deblurred-100nt --jobs-to-start 10 --trim-length 100 &
deblur workflow --seqs-fp raw-sequences.fna --output-dir ag-deblurred-125nt --jobs-to-start 10 --trim-length 125 &
deblur workflow --seqs-fp raw-sequences.fna --output-dir ag-deblurred-150nt --jobs-to-start 10 --trim-length 150 &

wait
cp -r ag-deblurred-100nt $cwd/
cp -r ag-deblurred-125nt $cwd/
cp -r ag-deblurred-150nt $cwd/

## qs -> qiita study id
curl -o qs850_qs10052_qs1448.biom ftp://ftp.microbio.me/pub/publications-files/american-gut/qs850_qs10052_qs1448.biom
curl -o $cwd/mapping_clemente_obregon_AGP2017simple.txt //ftp.microbio.me/pub/publications-files/american-gut/mapping_clemente_obregon_AGP2017simple.txt

source activate qiime191

merge_otu_tables.py -i qs850_qs10052_qs1448.biom,ag-deblurred-100nt/reference-hit.biom -o western_nonwestern.biom
cp western_nonwestern.biom $cwd/

curl -o blooms.fna https://raw.githubusercontent.com/knightlab-analyses/bloom-analyses/master/data/newbloom.all.fna
cut -c 1-100 blooms.fna > bloom100.fa
cut -c 1-125 blooms.fna > bloom125.fa
cut -c 1-150 blooms.fna > bloom150.fa

filter_otus_from_otu_table.py -i ag-deblurred-100nt/reference-hit.biom -e bloom100.fa -o otu_table_no_blooms_100nt.biom &
filter_otus_from_otu_table.py -i ag-deblurred-125nt/reference-hit.biom -e bloom125.fa -o otu_table_no_blooms_125nt.biom &
filter_otus_from_otu_table.py -i ag-deblurred-150nt/reference-hit.biom -e bloom150.fa -o otu_table_no_blooms_150nt.biom &
filter_otus_from_otu_table.py -i western_nonwestern.biom -e bloom100.fa -o western_nonwestern_nobloom.biom &
wait

cp otu_table_no_blooms_100nt.biom otu_table_no_blooms_125nt.biom otu_table_no_blooms_150nt.biom western_nonwestern_nobloom.biom $cwd/

for f in {otu_table_no_blooms_100nt.biom,otu_table_no_blooms_125nt.biom,otu_table_no_blooms_150nt.biom,western_nonwestern_nobloom.biom}
do
    fna=$(basename $f .biom).fna
    base=$(basename $f .biom)

    source activate qiime191
    # get a representative fasta file
    python -c "import biom; t = biom.load_table('$f'); f = open('$fna', 'w'); f.write(''.join(['>%s\n%s\n' % (i, i.upper()) for i in t.ids(axis='observation')]))"
    cp $fna $cwd/
        
    # insert the fragments into greengenes
    ./sepp-package/run-sepp.sh $fna $base -x 32
    cp ${base}*.tog.tre ${base}*.json $cwd/
    
    # map the fragments against greengenes 99%
    pick_otus.py -i $fna -o ${base}_gg_cr99 -m sortmerna -s 0.99 --threads 32
        
    source activate qiime2-2017.4
    # perform taxonomy assignment
    qiime tools import --type FeatureData[Sequence] --input-path $fna --output-path ${fna}.qza
    qiime feature-classifier classify-sklearn --i-classifier gg-13-8-99-515-806-nb-classifier.qza --i-reads ${fna}.qza --o-classification ${base}-taxonomy.qza
    uuid=$(qiime tools peek ${base}-taxonomy.qza | grep UUID | awk '{ print $2 }')
    unzip ${base}-taxonomy.qza
    biom add-metadata -i $f --observation-metadata-fp ${uuid}/data/taxonomy.tsv -o ${f}_tax.biom --observation-header "#OTUID",taxonomy --sc-separated taxonomy
    cp ${f}_tax.biom $cwd/

    source activate picrust
    # compute picrust profiles
    gg99_otu_map=${base}_gg_cr99/${base}_otus.txt
    table_expanded=$(basename ${f} .biom)_gg99.biom
    python expand.py $f ${gg99_otu_map} ${table_expanded}

    normed=$(basename ${table_expanded} .biom)_normed.biom
    normalize_by_copy_number.py -i ${table_expanded} -o ${normed}

    pred=$(basename ${normed} .biom)_pred.biom
    predict_metagenomes.py -i ${normed} -o ${pred} -a NSTI

    l3=$(basename ${pred} .biom)_L3.biom
    l2=$(basename ${pred} .biom)_L2.biom
    l1=$(basename ${pred} .biom)_L1.biom
    categorize_by_function.py -i ${pred} -c KEGG_Pathways -l 3 -o ${l3}
    categorize_by_function.py -i ${pred} -c KEGG_Pathways -l 2 -o ${l2}
    categorize_by_function.py -i ${pred} -c KEGG_Pathways -l 1 -o ${l1}
    cp NSTI $cwd/${pred}.nsti
    cp $l1 $cwd/
    cp $l2 $cwd/
    cp $l3 $cwd/
done
