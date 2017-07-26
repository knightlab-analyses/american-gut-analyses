set -x
set -e

source activate sk050-biom215

python split.py ../data/deblur_150nt_no_blooms.biom
python split.py ../data/ms.biom

python split_extremes.py ../data/deblur_150nt_no_blooms.biom ms.biom ../data/ag-cleaned.txt

export PYTHONPATH=../:$PYTHONPATH
# full
python ../eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom --right-table ../data/ms.biom --pa-right --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.biom --left-as-observations

# abx subset
python ../eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom.abx.biom --right-table ../data/ms.biom.abx.biom --pa-right --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.abx.biom --left-as-observations

# abx low
python ../eviiom/eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom.abx-low.biom --right-table ../data/ms.biom.abx-low.biom --pa-right --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.abx-low.biom --left-as-observations

# abx high
python ../eviiom/eviiom/drive.py blend --left-table ../data/deblur_150nt_no_blooms.biom.abx-high.biom --right-table ../data/ms.biom.abx-high.biom --pa-right --threads 4 --min-overlap 3 --output deblur_150nt_no_blooms.ms.eviiom.abx-high.biom --left-as-observations

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

python unifrac.py -i deblur_150nt_no_blooms.ms.eviiom.biom -t ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre -m weighted_unifrac -o deblur_150nt_no_blooms.ms.eviiom.weighted.pc &
python unifrac.py -i deblur_150nt_no_blooms.ms.eviiom.abx.biom -t ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre -m weighted_unifrac -o deblur_150nt_no_blooms.ms.eviiom.abx.weighted.pc &
python unifrac.py -i deblur_150nt_no_blooms.ms.eviiom.abx-low.biom -t ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre -m weighted_unifrac -o deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.pc &
python unifrac.py -i deblur_150nt_no_blooms.ms.eviiom.abx-high.biom -t ../data/AG_150nt_April_27_2017_new_sepp_placement.tog.tre -m weighted_unifrac -o deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.pc &
wait

source activate qiime191
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.weighted.L2.emp -m deblur_150nt_no_blooms.ms.eviiom.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.biom.L2.txt &
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.biom.L4.txt &
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.abx.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.abx.weighted.L2.emp -m deblur_150nt_no_blooms.ms.eviiom.abx.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx.biom.L2.txt &
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.abx.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.abx.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.abx.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx.biom.L4.txt &
wait

make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.L2.emp -m deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.L2.txt &
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.abx-low.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx-low.biom.L4.txt &
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.L2.emp -m deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.L2.txt &
make_emperor.py -i deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.pc -o deblur_150nt_no_blooms.ms.eviiom.abx-high.weighted.L4.emp -m deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.adiv.txt -t deblur_150nt_no_blooms.ms.eviiom.abx-high.biom.L4.txt &
wait
