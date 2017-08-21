set -e

input=$1
output=$2
njobs=$3

demux_to_persample.py --input ${input} --output ${output} --njobs ${njobs}

pushd ${output} > /dev/null

echo "sample-id,filename,direction" > MANIFEST

# this is not universally true, but likely is accurate
echo "{phred-offset: 33}" > metadata.yml

for f in *.fastq
do
    # there are filename expectations, so we need to munge to conform
    filename=$(basename ${f} .fastq)_IGNORED_L000_R1_001.fastq
    mv ${f} ${filename}
    gzip ${filename}
    echo "$(basename ${f} .fastq),${filename}.gz,forward" >> MANIFEST
done
popd > /dev/null