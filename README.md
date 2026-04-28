# MetaStrainerHelperScripts
Scripts that help with post processing MetaStrainer output. This will produce tables that could be used in creating data summaries and visualizations of the strain population structure and dynamics.


# Requirements
- CD-HIT run with the -d 0 option and -c clustering threshold matching the threshold used in Genotyping step of MetaStrainer.
- Folders for samples containing output of MetaStrainer Genotyping script under one directory.

# Running
python GenerateStrainAbundanceMatrix.py -s SampleList -d Folder -o StrainMatrixTables.tsv

-s takes a SampleList which is a file containing one sample id per line.
-d Folder is the parent directory containing MetaStrainer samples matching the names in the SampleList file.
-o StrainTables.tsv is the output matrix

python ClusterStrainFreqTable2.py -c CDHIT_Clusters -m StrainMatrixTables.tsv -o StrainClusters_table.txt
-c CDHIT_Clusters is the clustering output of CD-HIT, usually ending in .clstr. Make sure CD-HIT was run with the -d 0 option.
-m StrainMatrixTables.tsv should be the output table from the GenerateStrainAbundanceMatrix.py script
-o StrainClusters_table.txt is the output table with strain clusters at a given threshold. 



