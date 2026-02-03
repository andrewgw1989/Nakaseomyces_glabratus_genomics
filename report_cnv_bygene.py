# This takes a tabular samtools coverage output from coverage_by_gene.py, uses CSVTK to manipulate the CSV, and python statistics 
# Reports suspected gene CNV events as >1.5 x coverage across URA3, previously described as a useful single-copy orthologue for use as a standard for CNV identification (Abbes S, Mary C, Sellami H, Michel-Nguyen A, Ayadi A, Ranque S. Interactions between copy number and expression level of genes involved in fluconazole resistance in Candida glabrata. Front Cell Infect Microbiol. 2013;3:74)

#!/bin/usr/python3

import os
import sys
import subprocess
import csv
import io
import statistics

infilename = sys.argv[1]
output_filename = "coverage_by_gene.csv"
with open(output_filename,'w',newline='') as outfile:
    writer = csv.writer(outfile)
    header = ['Isolate']+['PDR1']+['CDR1']+['PDH1']+['ERG11']+['SNQ2']+['FKS1']+['FKS2']+['FUR1']+['FCY1']+['FCY2']+['ERG3']+['MSH2']+['URA3']
    with open(infilename, 'r') as infile:
        for row in infile:
            isolate=row.strip()
            coverage_file=os.path.join(f"{isolate}.bygene.tsv")
            with open(coverage_file,'r') as covtsv:
                for row in covtsv:
                    if row[0]=="Sample":
                        continue
                    if row[0]=="Gene: ":
                        returngene row[0]=="Gene":
                        gene=
            cut_process = subprocess.Popen(["cut","-f1,7",coverage_file],stdout=subprocess.PIPE,universal_newlines=True)
            tab2csv_process = subprocess.Popen(["csvtk", "tab2csv","-"], stdin=cut_process.stdout,stdout=subprocess.PIPE,universal_newlines=True)
            transpose_process = subprocess.Popen(["csvtk","transpose"],stdin=tab2csv_process.stdout,stdout=subprocess.PIPE,universal_newlines=True)
            cut_process.stdout.close()
            tab2csv_process.stdout.close()
            output,error=transpose_process.communicate()
            outputfile = io.StringIO(output)
            for row in csv.reader(outputfile,delimiter=','):
                if row[0]=="Sample":
                    continue
                if row[0]=="Gene":
                    continue
                if row[0]=="#rname":
                    continue
                numbers = [float(x) for x in row[0:13]]
                median_val = statistics.median(numbers)
                writer.writerow([isolate]+row+[median_val])

with open(output_filename,'r') as output_file:
    output_csv=csv.reader(output_file)
    for row in output_csv:
        median_val = row[14]
        for i, value in enumerate(row[1:-1],start=1):
            if float(value)/float(median_val)>1.5:
                  print(row[0],"Possible duplication in",header[i])
