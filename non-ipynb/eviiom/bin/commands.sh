set -x
set -e

source activate qiime2-2017.6

python split.py ../data/deblur_150nt_no_blooms.biom
python split.py ../data/ms.biom

python split_extremes.py ../data/deblur_150nt_no_blooms.biom ../data/ms.biom ../data/ag-cleaned.txt

export PYTHONPATH=../:$PYTHONPATH
# full
python ../eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom --right-table ../data/ms.biom --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.biom --left-as-observations

# abx subset
python ../eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom.abx.biom --right-table ../data/ms.biom.abx.biom --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.abx.biom --left-as-observations

# abx low
python ../eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom.abx-low.biom --right-table ../data/ms.biom.abx-low.biom --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.abx-low.biom --left-as-observations

# abx high
python ../eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom.abx-high.biom --right-table ../data/ms.biom.abx-high.biom --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.abx-high.biom --left-as-observations

python pd.py deblur_150nt_no_blooms.ms.eviiom.biom ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre ../data/identified_drugs.txt &
python pd.py deblur_150nt_no_blooms.ms.eviiom.abx.biom ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre ../data/identified_drugs.txt &
wait

python pd.py deblur_150nt_no_blooms.ms.eviiom.abx-low.biom ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre ../data/identified_drugs.txt &
python pd.py deblur_150nt_no_blooms.ms.eviiom.abx-high.biom ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre ../data/identified_drugs.txt &
wait

python summarize_taxonomy.py deblur_150nt_no_blooms.ms.eviiom.biom 4 &
python summarize_taxonomy.py deblur_150nt_no_blooms.ms.eviiom.abx.biom 4 &
wait

python summarize_taxonomy.py deblur_150nt_no_blooms.ms.eviiom.abx-low.biom 4 &
python summarize_taxonomy.py deblur_150nt_no_blooms.ms.eviiom.abx-high.biom 4 &
wait

qiime tools import --input-path deblur_150nt_no_blooms.ms.eviiom.biom --output-path deblur_150nt_no_blooms.ms.eviiom.biom.qza --type "FeatureTable[Frequency] % Properties(['uniform-sampling'])" 
qiime tools import --input-path deblur_150nt_no_blooms.ms.eviiom.abx.biom --output-path deblur_150nt_no_blooms.ms.eviiom.abx.biom.qza --type "FeatureTable[Frequency] % Properties(['uniform-sampling'])" 
qiime tools import --input-path deblur_150nt_no_blooms.ms.eviiom.abx-low.biom --output-path deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.qza --type "FeatureTable[Frequency] % Properties(['uniform-sampling'])" 
qiime tools import --input-path deblur_150nt_no_blooms.ms.eviiom.abx-high.biom --output-path deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.qza --type "FeatureTable[Frequency] % Properties(['uniform-sampling'])" 
qiime tools import --input-path ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre --output-path AG_150nt_April_27_2017_new_sepp_placement.tog.tre.qza --type Phylogeny[Rooted]

qiime state-unifrac weighted-unnormalized --i-table deblur_150nt_no_blooms.ms.eviiom.biom.qza --o-distance-matrix deblur_150nt_no_blooms.ms.eviiom.weighted --i-phylogeny AG_150nt_April_27_2017_new_sepp_placement.tog.tre.qza 
qiime state-unifrac weighted-unnormalized --i-table deblur_150nt_no_blooms.ms.eviiom.abx.biom.qza --o-distance-matrix deblur_150nt_no_blooms.ms.eviiom.abx.weighted --i-phylogeny AG_150nt_April_27_2017_new_sepp_placement.tog.tre.qza 
qiime state-unifrac weighted-unnormalized --i-table deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.qza --o-distance-matrix deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted --i-phylogeny AG_150nt_April_27_2017_new_sepp_placement.tog.tre.qza 
qiime state-unifrac weighted-unnormalized --i-table deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.qza --o-distance-matrix deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted --i-phylogeny AG_150nt_April_27_2017_new_sepp_placement.tog.tre.qza 

qiime diversity pcoa --i-distance-matrix deblur_150nt_no_blooms.ms.eviiom.weighted.qza --o-pcoa deblur_150nt_no_blooms.ms.eviiom.weighted.pc &
qiime diversity pcoa --i-distance-matrix deblur_150nt_no_blooms.ms.eviiom.abx.weighted.qza --o-pcoa deblur_150nt_no_blooms.ms.eviiom.abx.weighted.pc &
qiime diversity pcoa --i-distance-matrix deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.qza --o-pcoa deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.pc &
qiime diversity pcoa --i-distance-matrix deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.qza --o-pcoa deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.pc &
wait

full=$(qiime tools peek deblur_150nt_no_blooms.ms.eviiom.weighted.pc.qza | grep UUID | awk '{ print $2 }')
abx=$(qiime tools peek deblur_150nt_no_blooms.ms.eviiom.abx.weighted.pc.qza | grep UUID | awk '{ print $2 }')
abxlow=$(qiime tools peek deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.pc.qza | grep UUID | awk '{ print $2 }')
abxhigh=$(qiime tools peek deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.pc.qza | grep UUID | awk '{ print $2 }')

unzip deblur_150nt_no_blooms.ms.eviiom.weighted.pc.qza
unzip deblur_150nt_no_blooms.ms.eviiom.abx.weighted.pc.qza
unzip deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.pc.qza
unzip deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.pc.qza

source activate qiime191
make_emperor.py -i $full/data/ordination.txt -o deblur_150nt_no_blooms.ms.eviiom.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.biom.L4.txt &
make_emperor.py -i $abx/data/ordination.txt -o deblur_150nt_no_blooms.ms.eviiom.abx.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.abx.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx.biom.L4.txt &
make_emperor.py -i $abxlow/data/ordination.txt -o deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.L4.txt &
make_emperor.py -i $abxhigh/data/ordination.txt -o deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.L4.txt &
wait
