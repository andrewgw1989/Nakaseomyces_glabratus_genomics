# This script takes the following inputs: 
# (1) directory of input BAM file as command line argument; 
# (2) gene coordinates file (path hard-coded to working directory in this instance), a TSV (gene,region). Region is the nucleotide coordinates 

#!/usr/bin/python3
import sys
import os
import csv
import subprocess

bam_dir = sys.argv[1]

with open("gene_coords.tsv",newline='') as f:
    genecoords = list(csv.reader(f, delimiter='\t'))

with open("isolates.tsv","r") as input_file:
    for isolate in input_file:
        isolate = isolate.strip()
        bam_file=os.path.join(bam_dir, f"{isolate}.bam")
        output_path = f"{isolate}.output.txt"
        with open(output_path, "w") as out:
            print(f"Sample: {isolate}",file=out,flush=True)
            for line in genecoords:
                gene=line[0]
                region=line[1]
                print(f"Gene: {gene}",file=out,flush=True)
                cmd = ["samtools","coverage","-A","-w","32","-r",region,bam_file]
                subprocess.call(cmd, stdout=out, stderr=out)
