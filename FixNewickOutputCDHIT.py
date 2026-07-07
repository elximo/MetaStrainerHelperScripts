#Generated using ChatGPT general interface
#Jun 1 2026
#Blacksburg, VA
#Purpose: print tree Newick file using cluster ids in cluster file
#Input: Newick tree file
#Mapping File
#Output: Newick Tree with proper labels

#!/usr/bin/env python3

import re
import sys
import argparse

#tree_file = sys.argv[1]
#mapping_file = sys.argv[2]
#output_file = sys.argv[3]

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", required=True, help="Input Newick tree file (tested with RaXML)")
parser.add_argument("-o","--output", required=True, help="Newick output file with update labels")
parser.add_argument("-m","--mapping", required=True, help="CDHIT cluster file")

args = parser.parse_args()

mapping_file = args.mapping
tree_file = args.input
output_file = args.output

# Build mapping dictionary
mapping = {}

with open(mapping_file) as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        # Split only on the first underscore
        #Jul 06 2026
        #Bug processing
        #Make sure others are using the updated output of ClusterStrainFreqTable2.py without the extra "_" after Cluster
        cluster_id, seq_id = line.split("_", 1)

        mapping[seq_id] = f"{cluster_id}_{seq_id}"

print(f"Loaded {len(mapping)} mappings")

# Read tree
with open(tree_file) as f:
    newick = f.read()

# Replace labels
for seq_id, cluster_id in mapping.items():

    # Match a taxon name occurring between '(' or ','
    # and followed by ':' ')' ',' or ';'
    pattern = rf'(?<=[(,]){re.escape(seq_id)}(?=[:),;])'

    newick = re.sub(pattern, cluster_id, newick)

# Write result
with open(output_file, "w") as f:
    f.write(newick)

print(f"Wrote {output_file}")