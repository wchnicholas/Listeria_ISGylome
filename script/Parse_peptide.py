#!/usr/bin/python
import os
import sys
import glob
from collections import defaultdict

def read_MS_rawdata(file_rawdata):
  infile  = open(file_rawdata, 'r')
  MS_dict = defaultdict(list)
  for line in infile.xreadlines():
    if 'C: Cluster' in line: continue
    line = line.rstrip().rsplit("\t")
    clusterid = line[0]
    proteinid = line[1]
    peptide   = line[6][10:-10]
    if '_' in proteinid:
      print "Ignored protein ID: %s" % proteinid
      continue
    else:
      MS_dict[clusterid].append(peptide)
  infile.close()
  return MS_dict

def print_alignment(MS_dict, file_out):
  for clusterID in MS_dict.keys():
    alnfilename  = file_out.replace('XXX',clusterID).replace(' ','')
    logofilename = alnfilename.replace('result/','graph/').replace('.aln','.png')
    print "writing file: %s" % alnfilename
    outfile = open(alnfilename,'w')
    for seq in MS_dict[clusterID]:
      outfile.write(seq+"\n")
    outfile.close()
    print "writing file: %s" % logofilename
    os.system("/Users/wchnicholas/Bioinformatics/weblogo-3.6.0/weblogo -A protein -f "+alnfilename+ \
              " -c chemistry -U probability -X NO -Y NO --resolution 600 -F png -s large --aspect-ratio 2 -o "+logofilename)

def main():
  file_rawdata    = "data/MS_ISG15_Raw.tsv"
  file_out        = 'result/Peptide_XXX.aln'
  MS_dict         = read_MS_rawdata(file_rawdata)
  print_alignment(MS_dict, file_out)

if __name__ == "__main__":
  main()
