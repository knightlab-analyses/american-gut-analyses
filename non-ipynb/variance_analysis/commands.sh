headpos ()
{
    echo `head -n 1 $1 | tr "\t" "\n" | egrep -n "^$2\$" | cut -d ':' -f 1`
}

source activate py36-base

package=$HOME/scratch/ag-manuscript-package
mkdir -p ${package}/1250/distance

curl -o i${package}/data_dictionary.csv ftp://ftp.microbio.me/AmericanGut/manuscript-package/data_dictionary.csv
sed 's/^M/\n/g' ${package}/data_dictionary.csv > ${package}/data_dictionary_corrected.csv
sed -i 's/alzhemiers/alzheimers/g' ${package}/data_dictionary_corrected.csv

curl -o ${package}/1250/ag_map_with_alpha.txt ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/ag_map_with_alpha.txt
curl -o ${package}/1250/distance/unweighted.txt.gz ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/distance/unweighted.txt.gz
curl -o ${package}/1250/distance/weighted-normalized.txt.gz ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/distance/weighted-normalized.txt.gz
curl -o ${package}/1250/distance/bray_curtis.txt.gz ftp://ftp.microbio.me/AmericanGut/manuscript-package/1250/distance/bray_curtis.txt.gz

# R read.table is not being nice.
sed -i 's/^10317/x10317/' ${package}/1250/ag_map_with_alpha.txt

mkdir -p $HOME/ag-manuscript-adonis/
./clean_map_agp.py --mapping ${package}/1250/ag_map_with_alpha.txt --data-dictionary ${package}/data_dictionary_corrected.csv --output $HOME/ag-manuscript-adonis/maps_final_state

map=$HOME/ag-manuscript-adonis/maps_final_state/ag_map_with_alpha.txt.quartiles.tsv
iters=1000
package=$HOME/scratch/ag-manuscript-package

subtemplate_cc=submission.template
subscript_dir=submission-scripts-subset-mappings
mkdir -p ${subscript_dir}

subset_mappings=$HOME/scratch/subset-mappings
mkdir -p ${subset_mappings}

rm array_details.txt
count=-1

mkdir -p {1250,2500,5000}/{bray_curtis,unweighted,weighted-normalized}

for category in $(head -n 1 ${map} | tr "\t" "\n" | grep -v "^#")
do
	# create a mapping file that only corresponds to the samples and category being examined
    col=$(headpos ${map} ${category})
    cut -f 1,${col} ${map} | grep -v "  nan$" > ${subset_mappings}/${category}.txt

    for metric in {bray_curtis,unweighted,weighted-normalized}
    do
        for rare in {1250,2500,5000}
        do
            ((count++))
            echo -e "${count}\t${rare}\t${metric}\t${category}\t${iters}" >> array_details.txt
        done

    done
done
sbatch -a 0-${count} submission.template
echo "count: ${count}"
