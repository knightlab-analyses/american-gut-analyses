#
# Getting mapping file and data data_dictionary + some data cleaning
#

curl -o ag_map_with_alpha.txt ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/ag_map_with_alpha.txt
curl -o data_dictionary.csv ftp://ftp.microbio.me/AmericanGut/manuscript-package/data_dictionary.csv .

# open data_dictionary and replace
:%s/^M/\r/g
:%s/alzhemiers/alzheimers/g

#
# From the full map file, just get the alpha diversity columns we want to tests,
# defined in alpha_columns.txt
#

./dataExtractor.sh ag_map_with_alpha.txt alpha_columns.txt > alpha_div.tsv

#
# Generating the "clean" mapping files for effect size calculations
#

./clean_map_agp.py --mapping ag_map_with_alpha.txt --data-dictionary data_dictionary.csv --output maps1000
for f in `find ./ -iname '*quartiles*' | grep './/maps'`; do echo $f; head -n 1 $f | awk '{print NF}'; done
  # .//maps1000/ag_map_with_alpha.txt.quartiles.tsv
  # 361
  # .//maps2000/ag_map_with_alpha.txt.quartiles.tsv
  # 149
  # .//maps5000/ag_map_with_alpha.txt.quartiles.tsv
  # 126

#
# Alpha diversity calculations/commands
#

./effect-size.py --mappings maps1000/ag_map_with_alpha.txt.quartiles.tsv --alphas alpha_div.tsv --output alpha1000/
./effect-size.py --mappings maps2000/ag_map_with_alpha.txt.quartiles.tsv --alphas alpha_div.tsv --output alpha2000/
./effect-size.py --mappings maps5000/ag_map_with_alpha.txt.quartiles.tsv --alphas alpha_div.tsv --output alpha5000/

./summarize_mdfdr.py --input-fp alpha1000/ --output-fp results1000
./summarize_mdfdr.py --input-fp alpha2000/ --output-fp results2000
./summarize_mdfdr.py --input-fp alpha5000/ --output-fp results5000

./clean_map_agp.py --mapping ag_map_with_alpha.txt --data-dictionary data_dictionary.csv --output maps_final
./effect-size.py --alphas alpha_div.tsv --mappings maps_final/ag_map_with_alpha.txt.quartiles.tsv --output alpha_final
./summarize_mdfdr.py --input-fp alpha_final/ --output-fp alpha_results_final

./clean_map_agp.py --mapping ag_map_with_alpha.txt --data-dictionary data_dictionary.csv --output maps_final_state
./effect-size.py --alphas alpha_div.tsv --mappings maps_final_state/ag_map_with_alpha.txt.quartiles.tsv --output alpha_final_state
./summarize_mdfdr.py --input-fp alpha_final_state/ --output-fp alpha_results_final_state

#
# Beta diversity file retrival and calculations
# Note that due to the permutations this might take days, even using 32 jobs
#

curl -o unweighted.txt.gz ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/distance/unweighted.txt.gz
curl -o weighted-normalized.txt.gz ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/distance/weighted-normalized.txt.gz
gunzip *.gz

./effect-size.py --mappings maps_final/ag_map_with_alpha.txt.quartiles.tsv --betas unweighted.txt --output beta_final_5K --jobs 32 --permutations 5000
./effect-size.py --mappings maps_final/ag_map_with_alpha.txt.quartiles.tsv --betas weighted-normalized.txt --output beta_final_5K --jobs 32 --permutations 5000

./summarize_mdfdr.py --input-fp beta_final_5K --output-fp beta_results_final_clean/5K --beta-files
