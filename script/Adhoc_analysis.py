#!/usr/bin/python
import os
import sys
import glob
from Bio import SeqIO
from collections import defaultdict, Counter

def reading_aln(file_aln):
  seq_dict = {}
  for record in SeqIO.parse(file_aln,"fasta"):
    ID    = str(record.id)
    seq   = str(record.seq)
    seq_dict[ID] = seq
  return seq_dict

def reading_taxcat(file_tax):
  infile = open(file_tax, 'r')
  taxcat_dict = {}
  for line in infile.xreadlines():
    if 'taxid' in line: continue
    line = line.rstrip().rsplit("\t")
    taxcat_dict[line[1]] = line[-1]
  infile.close()
  return taxcat_dict

def extract_site_info(seq_dict, uniprot, site):
  ref_ID   = [ID for ID in seq_dict if uniprot in ID]
  assert(len(ref_ID) == 1)
  ref_ID   = ref_ID[0]
  ref_seq = seq_dict[ref_ID]
  ref_resi  = 0
  site_dict = {}
  for n in range(len(ref_seq)):
    if ref_seq[n] != '-':
      ref_resi += 1
      if str(ref_resi) == site:
        for ID in seq_dict.keys():
          site_dict[ID] = seq_dict[ID][n]
  return site_dict

def write_aln_ID_rename(file_aln, taxcat_dict, site_dict, out_aln):
  print "Writing: %s" % out_aln
  outfile = open(out_aln, 'w')
  counttotal_ISG_yes = {'yes':0,'no':0}
  counttotal_ISG_no  = {'yes':0,'no':0}
  for record in SeqIO.parse(file_aln,"fasta"):
    ID     = str(record.id)
    taxid  = ID.rsplit('|')[0].rsplit('-')[0].rsplit('_')[1]
    seq    = str(record.seq)
    site   = site_dict[ID]
    taxcat = taxcat_dict[taxid]
    if taxcat == 'Y':
      if site == 'K': counttotal_ISG_yes['yes'] += 1
      else: counttotal_ISG_yes['no'] += 1
    elif taxcat == 'N':
      if site == 'K': counttotal_ISG_no['yes'] += 1
      else: counttotal_ISG_no['no'] += 1
    else: 
      print "ERROR: ISG15 no classified"
      sys.exit()
    outfile.write(">"+ID+"__"+site+"||"+taxcat+"||"+"\n"+seq+"\n")
  outfile.close()
  return counttotal_ISG_yes, counttotal_ISG_no

def compile_count(counttotal_ISG_yes, counttotal_ISG_no, out_count):
  outfile = open(out_count,'w')
  outfile.write("\t".join(['TaxClass', 'Lys', 'non-Lys'])+"\n"+
                "\t".join(map(str,['Species with ISG15', counttotal_ISG_yes['yes'], counttotal_ISG_yes['no']]))+"\n"+
                "\t".join(map(str,['Species without ISG15', counttotal_ISG_no['yes'], counttotal_ISG_no['no']]))+"\n")
  print "Finished writing %s" % out_count

def main():
  sites  = ['Q9JLN9-2066', 'Q80W47-198','A2AH22-175']
  taxcat_dict = reading_taxcat('data/taxID_ISGylation_class.csv')
  for site in sites:
    uniprot, site = site.rsplit('-')
    print "Analyzing %s site %s" % (uniprot, site)
    file_aln  = 'Fasta/Ortholog_'+uniprot+'.aln'
    out_aln   = 'Fasta/Ortholog_'+uniprot+'_'+site+'.aln'
    out_count = 'Tree/Count_Lys_'+uniprot+'_'+site+'.tsv'
    seq_dict  = reading_aln(file_aln)
    site_dict = extract_site_info(seq_dict, uniprot, site)
    counttotal_ISG_yes, counttotal_ISG_no = write_aln_ID_rename(file_aln, taxcat_dict, site_dict, out_aln)
    compile_count(counttotal_ISG_yes, counttotal_ISG_no, out_count) 

if __name__ == "__main__":
  main()
