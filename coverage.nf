# A pipeline for reporting suspected copy-number variants at the chromosome level, using samtools coverage
# Reports suspected CNV based on chromosomal coverage > 1.5 x median coverage across all chromosomes

#!/usr/bin/env nextflow

params.isolates = 'isolates.list'

process coverage_by_chromosome {
    tag "$isolate"
    publishDir 'output_bysample', mode: 'copy'
    cache 'lenient'
    input:
        val isolate
    output:
        path "${isolate}_cov.csv"
    script:
    """
    samtools coverage [path to bam]/{isolate}.bam | cut -f1,7 | csvtk tab2csv | csvtk transpose > ${isolate}_cov.csv
    """
}

process add_samplename {
    publishDir 'output_bysample',mode:'copy'
    cache 'lenient'
    input:
        path cov_csv
    output:
        path "*_named.csv"
    script:
    """
#!/usr/bin/env python3
import os
import csv
import statistics
from statistics import median
filename='$cov_csv'
isolate=os.path.basename(filename).replace('_cov.csv','')
outname=f"{isolate}_named.csv"
with open(filename,'r') as f, open(outname,'w',newline='') as out:
    reader=csv.reader(f)
    writer=csv.writer(out)
#    writer.writerow(["Sample"]+header+["Median"])
    for row in reader:
        if row[0]=="NC_088951.1":
            continue
        numbers = [float(x) for x in row[1:13]]
        median_val = statistics.median(numbers)
        writer.writerow([isolate]+row+[median_val])

    """
}

process concatenate {
    publishDir 'output_aggregated', mode: 'copy'
    cache 'lenient'
    input:
        path namedcsvs
    output:
        path "coverage_by_chromosome.csv"
    script:
    """
    echo "Isolate,ChrA,ChrB,ChrC,ChrD,ChrE,ChrF,ChrG,ChrH,ChrI,ChrJ,ChrK,ChrL,ChrM,Median" > coverage_by_chromosome.csv
    cat ${namedcsvs} >> coverage_by_chromosome.csv
    """
}

process output_duplicates {
    publishDir 'output_aggregated', mode: 'copy'
    cache 'lenient'
    input:
        path inputfile
    output:
        path "possible_duplicates.csv"
    script:
    """
    #!/usr/bin/env python3
    import csv
    infile_path = "$inputfile"
    with open(infile_path, 'r') as infile:
        with open ("possible_duplicates.csv","w",newline="") as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            writer.writerow(["Sample","Chromosome","Coverage","Coverage/Median"])
            header = next(reader)
            chrom_names = header[1:-1]
            for row in reader:
                isolate = row[0]
                median = float(row[14])
                for index, chrom in enumerate(chrom_names,start=1):
                    try:
                        value = float(row[index])
                    except ValueError:
                        continue
                    if value/median > 1.5:
                        writer.writerow([isolate,chrom,value,value/median])
    """
}

workflow {
    isolates_ch = Channel
                        .fromPath(params.isolates)
                        .splitText()
                        .map { it.trim() }
                        .filter { it }

    coverage_by_chromosome( isolates_ch )
    
    add_samplename( coverage_by_chromosome.out )


    namedcsvs_ch = Channel
                         .fromPath('output_bysample/*_named.csv')
                         .collect()
   
    concatenate( namedcsvs_ch )

    output_duplicates(concatenate.out)

}



