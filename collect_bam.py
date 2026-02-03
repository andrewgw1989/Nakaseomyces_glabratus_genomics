# Custom python script for collecting binary alignment map files from mdu-phl/bohra (bohra2) output

#!/bin/usr/python3/

import os
import shutil
import re

tsv1_path = {path to nextflow trace} 
tsv2_path = {path to isolates.list} 
work_base = {path to work directory}
destination_folder = {bam destination folder}
source_filename = "snps.bam"
source_file_index = "snps.bam.bai"

with open(tsv2_path, 'r') as sample_file:
    sample_names = [line.strip() for line in sample_file if line.strip()]

with open(tsv1_path, 'r') as trace_file:
    headers = trace_file.readline().strip().split('\t')
    
    for line in trace_file:
        fields = line.strip().split('\t')
        text = fields[3]
        sample = text.split('(')[-1].rstrip(')')
        short_hash = fields[1]

        if not re.search(r"RUN_SNPS:SNIPPY", line):
            continue 
        if sample not in sample_names:
            continue
        
        subdir = short_hash.split('/')[0]
        partial_hash = short_hash.split('/')[1]

        full_path_prefix = os.path.join(work_base, subdir)
        matched_dir = None
        
        for dirname in os.listdir(full_path_prefix):
            if dirname.startswith(partial_hash):
                matched_dir = os.path.join(full_path_prefix, dirname)
                break

        if not matched_dir:
            print(f"No matching directory for hash {short_hash}")
            continue
        src_bam = os.path.join(matched_dir, sample, source_filename)
        dest_bam = os.path.join(destination_folder, f"{sample}.bam")

        if os.path.exists(src_bam):
            shutil.copy(src_bam, dest_bam)
            print(f"Copied {src_bam} -> {dest_bam}")
        else: 
            print(f"{source_filename} not found at {src_bam}")

