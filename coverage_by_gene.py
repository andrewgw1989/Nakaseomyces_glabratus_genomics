# This script takes the following inputs: 
# (1) directory of input BAM file as command line argument; 
# (2) gene coordinates file (path hard-coded to working directory in this instance), a TSV (gene,region). Region is the nucleotide coordinates 

#!/usr/bin/python3
import sys
import os
import csv
import subprocess
import io

bam_dir = sys.argv[1]

with open("gene_coords.tsv",newline='') as f:
    genecoords = list(csv.reader(f, delimiter='\t'))

with open("isolates.list","r") as input_file:
    for isolate in input_file:
        isolate = isolate.strip()
        bam_file=os.path.join(bam_dir, f"{isolate}.bam")
        output_path = f"{isolate}.bygene.tsv"
        
        with open(output_path, "w") as out:
             header_written=False
            
            for line in genecoords:
                gene=line[0]
                region=line[1]
                #print(f"Gene: {gene}",file=out,flush=True)
                cmd = ["samtools","coverage","-r",region,bam_file]
                result = subprocess.call(cmd, capture_output=True,text=True,check=True)
                
                for line in result.stdout.strip().split('\n'):
                    if line.startwith("rname"): 
                        if not header_written:
                            out.write('Gene\t'+line+'\n')
                            header_written=True
                        else:
                            out.write(f"{gene}\t{line}\n")

