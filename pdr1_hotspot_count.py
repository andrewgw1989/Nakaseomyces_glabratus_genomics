# Count mutations occuring in PDR1 'hot spot' domains 

#!/usr/bin/python3

import os
import subprocess
import csv
import sys
import os.path
import re

inputfile=sys.argv[1]
hotspot_muts = sys.argv[2]

with open(hotspot_muts,'r') as mutfile:
    mutation_data = list(csv.reader(mutfile,delimiter='\t'))

print('Sample','DBD_count','ID_count','MHR_count','AD_count',sep='\t')

with open(inputfile,'r') as samplefile:
    for sample in samplefile:
        sample = sample.strip()
        DBD_count = ID_count = MHR_count = AD_count = 0

        for row in mutation_data:
            if sample in row:
                domain= row[3]
                if domain=='DBD':
                    DBD_count += 1
                elif row[3]=='ID':
                    ID_count += 1
