# Custom python scripts for extracting PDR1 mutations from global dataset
# 1.	Extract missense PDR1 mutations

import os
import subprocess
import csv
import sys
import os.path

listfile = sys.argv[1]

with open(listfile,'r') as input_file:
    for isolate in input_file:
        isolatename=isolate.strip()
        reportfile=os.path.join(f"{isolatename}_out.run",'report.tsv')
        if os.path.isfile(reportfile):
            with open(reportfile,'r') as report:
                reportread = csv.reader(report, delimiter = '\t')
                for row in reportread:
                    if row[0]=="#ariba_ref_name":
                        continue
                    elif row[17] =="1" and row[18]!='.':
                        print(isolatename,row[0],row[18],row[29], sep='\t')
                    else:
                        continue
        else:
            continue
