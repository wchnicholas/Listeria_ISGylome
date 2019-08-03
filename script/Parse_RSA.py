#!/usr/bin/python
import os
import sys
import glob
import numpy as np
from collections import defaultdict

def reading_RSA(infile_RSA):
  infile = open(infile_RSA,'r')
  RSA_dict = defaultdict(list)
  for line in infile.xreadlines():
    if 'UniProt_ID' in line: continue
    line = line.rstrip().rsplit("\t")
    RSA_dict["|".join(line[1::])].append(line[0])
  infile.close()
  return RSA_dict

def filtering_RSA(RSA_dict, outfile_RSA):
  print "Writing: %s" % outfile_RSA
  outfile = open(outfile_RSA, 'w')
  outfile.write("\t".join(['Type','UniProt_ID','position','PDB','PDB_chain','PDB_resi','RSA'])+"\n")
  for info in RSA_dict.keys():
    newinfo = info.rsplit('|')
    if float(newinfo[-1]) > 1:
      newinfo = "\t".join(newinfo[0:-1])+"\t"+'1.0'
    else: 
      newinfo = "\t".join(newinfo)
    if len(RSA_dict[info]) > 1:
      outfile.write('ISG15'+"\t"+newinfo+"\n")
    if len(RSA_dict[info]) == 1:
      outfile.write(RSA_dict[info][0].replace('All','Other')+"\t"+newinfo+"\n")
  outfile.close()

def main():
  infile_RSA   = 'result/ISG15_Lys_RSA.tsv'
  outfile_RSA  = 'result/ISG15_Lys_RSA_filtered.tsv'
  RSA_dict = reading_RSA(infile_RSA)
  filtering_RSA(RSA_dict, outfile_RSA)
  
if __name__ == "__main__":
  main()
