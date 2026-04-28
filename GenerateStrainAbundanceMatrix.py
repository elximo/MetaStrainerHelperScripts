#Date: 16th of Jun, 2025
#Location: Blacksburg, VA (USA)
#Purpose: Create Abundance abundanceMatrix from strain frequencies
#Input: Sample Names and sample name
#output: N strain fasta files


import os
import argparse
import sys
import traceback
import time


parser = argparse.ArgumentParser()

parser.add_argument("-s","--samples", required=True, help="List of samples")
parser.add_argument("-d","--directory", required=True,help="Folder containing MetaStrainer genotyped samples")
parser.add_argument("-o","--outputfile", default="StrainsAbundanceMatrix.txt", help="Abundance file")

args = parser.parse_args()

ErrorDebug = open("AbunDanceMatrixError.txt","w",buffering=4)

if not os.path.exists(args.directory):
	sys.exit("Input path of MetaStrainer output is wrong")


#Loading list of Samples
sampleList = []
with open(args.samples, 'r') as samples_file:
	for line in samples_file:    
		sampleList.append(line.strip())

#Looping  through user sample
abundanceMatrix = {}  # {concatStrainName: {sample: abundance}}
samplesFound = []

for sample in os.listdir(args.directory):
	if sample not in sampleList:
		continue

	folderPath = os.path.join(args.directory, sample)
	if not os.path.isdir(folderPath):
		print("Encountered error with Sample: %s Folder not found"%(sample))
		ErrorDebug.write("Encountered error with Sample: %s Folder not found"%(sample))
		continue

	
	#Convert to "D35_L2_3_S36_L002_ConcatStrain1"
	filename = "newkey_" + sample + "_.txt"
	filePath = os.path.join(folderPath, filename)

	if not os.path.isfile(filePath):
		print("Encountered error with Sample: %s Accessing frequency file %s "%(sample,filename))
		ErrorDebug.write("Encountered error with Sample: %s Accessing frequency file %s\n"%(sample,filename))
		continue

	samplesFound.append(sample)

	with open(filePath, 'r') as strain_frequency_file:
		for line in strain_frequency_file:
			lineContents = line.strip().split()
			
			strain = lineContents[0]
			abundance = float(lineContents[1]) * 100
			
			#Strain Name in CDHIT is for the concatenated strain so change to match Concat strain name
			#e.g. >D35_L3_2_S83_L004_ConcatStrain1
			concatStrainName = sample + "_Concat" + strain.capitalize()

			if concatStrainName not in abundanceMatrix:
				abundanceMatrix[concatStrainName] = {}

			abundanceMatrix[concatStrainName][sample] = round(abundance, 2)

rows = sorted(abundanceMatrix.keys())
samplesFound = sorted(samplesFound)

with open(args.outputfile, 'w') as writeMatrix: 
	# Header row
	writeMatrix.write("\t" + "\t".join(samplesFound) + "\n")

	# Matrix rows
	for row in rows:
		writeMatrix.write(row)
		for sample in samplesFound:
			value = abundanceMatrix[row].get(sample, "")
			writeMatrix.write("\t" + (str(value) if value != "" else "0.0"))
		writeMatrix.write("\n")

ErrorDebug.close()