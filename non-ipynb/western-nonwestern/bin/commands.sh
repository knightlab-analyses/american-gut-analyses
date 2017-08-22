source activate qiime2-2017.4

# Let's import our files from the initial processing into QIIME2 artifacts
qiime tools import --type FeatureTable[Frequency] --input-path western_nonwestern_nobloom.biom --output-path western_nonwestern_nobloom.qza
qiime tools import --type Phylogeny[Rooted] --input-path western_nonwestern_nobloom_placement.tog.tre --output-path western_nonwestern_nobloom_placement.tog.qza

# ...and let's grab the mapping file for the analysis which was not downloaded in the initial processing
curl -o mapping_clemente_obregon_AGP2017simple.txt ftp://ftp.microbio.me/pub/publications-files/american-gut/mapping_clemente_obregon_AGP2017simple.txt

# Now, we'll compute UniFrac:
    
qiime feature-table rarefy --i-table western_nonwestern_nobloom.qza --o-rarefied-table western_nonwestern_nobloom_even1250.qza --p-sampling-depth 1250
qiime state-unifrac unweighted --i-table western_nonwestern_nobloom_even1250.qza --o-distance-matrix western_nonwestern_nobloom_even1250_dm.qza --i-phylogeny western_nonwestern_nobloom_placement.tog.qza

# Now, we're going to filter down to the samples of interest. The sample
# information files for the studies are not entirely consistent with each other
# unfortunately. The series of commands were executed using a QIIME 1.9.1
# environment.

# filtering OTU table for balance analysis to include a healthy subset of individuals over 3 years of age. 
mkdir -p data
source activate qiime191
filter_samples_from_otu_table.py -i western_nonwestern_nobloom.biom -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_diabetes:Yes,no_data' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db.biom

filter_samples_from_otu_table.py -i data//meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db.biom -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_ibd:Yes,no_data' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd.biom 

filter_samples_from_otu_table.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd.biom -s 'subset_antibiotic_history:Yes,no_data' -m mapping_clemente_obregon_AGP2017simple.txt -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd_abx.biom

# only considered bmi for AGP samples 17 years and older because BMI is more complicated at younger ages. Created a new metadata column for this called 'subset_bmi_meta_analysis'.

filter_samples_from_otu_table.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd_abx.biom -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_bmi_meta_analysis:Yes' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd_abx_bmi.biom 

filter_samples_from_otu_table.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd_abx_bmi.biom -m mapping_clemente_obregon_AGP2017simple.txt -s 'age_keep_meta_analysis:Yes' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_db_ibd_abx_bmi_3yrs.biom 

uuid=$(qiime tools peek western_nonwestern_nobloom_even1250_dm.qza | grep -i uuid | awk '{ print $2 }')
source activate qiime191

# now repeating this filtering on distance matrix to make PCoA
unzip western_nonwestern_nobloom_even1250_dm.qza
filter_distance_matrix.py -i $uuid/data/distance-matrix.tsv -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_diabetes:Yes,no_data' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db.dm.txt 

filter_distance_matrix.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db.dm.txt -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_ibd:Yes,no_data' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd.dm.txt 

filter_distance_matrix.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd.dm.txt -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_antibiotic_history:Yes,no_data' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx.dm.txt 

filter_distance_matrix.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx.dm.txt -m mapping_clemente_obregon_AGP2017simple.txt -s 'subset_bmi_meta_analysis:Yes' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi.dm.txt 

filter_distance_matrix.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi.dm.txt -m mapping_clemente_obregon_AGP2017simple.txt -s 'age_keep_meta_analysis:Yes' -o data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi_3yrs.dm.txt 

principal_coordinates.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi_3yrs.dm.txt -o data/pc_meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi_3yrs.dm.txt 

make_emperor.py -i data/pc_meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi_3yrs.dm.txt -m mapping_clemente_obregon_AGP2017simple.txt -o emperor_3yrs

compare_categories.py -i data/meta_ag4.27.17_qs850_qs10052_qs1448_100nt_even1250_nobloom_unweighted_db_ibd_abx_bmi_3yrs.dm.txt -m mapping_clemente_obregon_AGP2017simple.txt -c life_style_2 -o emperor_3yrs/permanova --method permanova
