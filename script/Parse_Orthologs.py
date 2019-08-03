#!/usr/bin/python
import os
import sys
import glob
import uniprot
from Bio import SeqIO
from collections import defaultdict, Counter

def read_MS_rawdata(file_rawdata):
  infile  = open(file_rawdata, 'r')
  MS_dict = defaultdict(dict)
  for line in infile.xreadlines():
    if 'C: Cluster' in line: continue
    line = line.rstrip().rsplit("\t")
    clusterid = line[0]
    proteinid = line[1]
    position  = int(line[2])
    if '_' in proteinid:
      print "Ignored protein ID: %s" % proteinid
      continue
    else:
      uniprotid = proteinid
      if uniprotid not in MS_dict: MS_dict[uniprotid] = {'Position':[]}
      MS_dict[uniprotid]['Position'].append(position)
  infile.close()
  return MS_dict

def reading_align(file_align):
  seq_dict = {}
  for record in SeqIO.parse(file_align,"fasta"):
    ID    = str(record.id)
    seq   = str(record.seq)
    seq_dict[ID] = seq
  return seq_dict

def analyze_resi_con(seq_dict, uniprot_id, MS_dict, aas, outfile):
  positions = list(set(MS_dict[uniprot_id]['Position']))
  ref_ID    = [ID for ID in seq_dict.keys() if uniprot_id in ID]
  print uniprot_id
  if len(ref_ID) > 1:
    print "ERROR: Two sequences match reference ID: %s" % uniprot_id
    sys.exit()
  print ref_ID
  ref_ID    = ref_ID[0]
  ref_seq   = seq_dict[ref_ID]
  ref_resi  = 0
  for n in range(len(ref_seq)):
    if ref_seq[n] != '-':
      ref_resi += 1
      if ref_resi in positions:
        if ref_seq[n]!='K': print "SKIP: Position %i in %s is not Lys" % (ref_resi, uniprot_id); continue
        variations = Counter([seq_dict[ID][n] for ID in seq_dict.keys() if seq_dict[ID][n] in aas])
        var_counts = [float(variations[aa])/float(sum(variations.values())) for aa in aas]
        outfile.write("\t".join(map(str,['ISG15', uniprot_id, ref_resi]+var_counts))+"\n")
      elif ref_seq[n]=='K':
        variations = Counter([seq_dict[ID][n] for ID in seq_dict.keys() if seq_dict[ID][n] in aas])
        var_counts = [float(variations[aa])/float(sum(variations.values())) for aa in aas]
        outfile.write("\t".join(map(str,['Other', uniprot_id, ref_resi]+var_counts))+"\n")

def mafft_alignment(file_fasta, file_align):
  os.system('mafft --anysymbol '+file_fasta+' > '+file_align)

def main():
  filenames = glob.glob('Fasta/*.fa')
  file_rawdata = "data/MS_ISG15_Raw.tsv"
  file_con     = "result/ISG15_Lys_con.tsv"
  MS_dict      = read_MS_rawdata(file_rawdata)
  aas = ['E','D','R','K','H','Q','N','S','T','P','G','C','A','V','I','L','M','F','Y','W','-']
  outfile = open(file_con, 'w')
  outfile.write("\t".join(['Type', 'UniProt_ID', 'position', "\t".join(aas)])+"\n")
  for file_fasta in filenames:
    uniprot_id = file_fasta.rsplit('_')[1].rsplit('.')[0]
    file_align = file_fasta.replace('.fa','.aln')
    if len([line for line in open(file_fasta,'r').xreadlines()]) <= 2: continue
    if len(glob.glob(file_align)) == 0: mafft_alignment(file_fasta, file_align)
    seq_dict   = reading_align(file_align)
    analyze_resi_con(seq_dict, uniprot_id, MS_dict, aas, outfile)
  outfile.close()
    
  
'''
1. use mafft to align
2. search for the sites
3. look at conservation
4. taxonomy classification
'''

if __name__ == "__main__":
  main()
