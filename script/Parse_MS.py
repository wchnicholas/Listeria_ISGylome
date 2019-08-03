#!/usr/bin/python
import os
import sys
import glob
import pprint
import uniprot
from PyEntrezId import Conversion
from collections import defaultdict

sys.path.insert(0, 'metaphors_api')
import dbClient

def read_MS_rawdata(file_rawdata):
  infile  = open(file_rawdata, 'r')
  MS_dict = defaultdict(dict)
  for line in infile.xreadlines():
    if 'C: Cluster' in line: continue
    line = line.rstrip().rsplit("\t")
    clusterid = line[0]
    proteinid = line[1]
    if '_' in proteinid: 
      print "Ignored protein ID: %s" % proteinid
      continue
    else:
      uniprotid = proteinid
      MS_dict[uniprotid] = {}
  infile.close()
  return MS_dict

def write_seq_to_file(m, taxid, protid, outfile):
  fasta = m.get_fasta(protid)
  ID  = fasta.rsplit("\n")[0]
  seq = ''.join(fasta.rsplit("\n")[1::])
  outfile.write('>taxid_'+str(taxid)+'|'+ID.replace('>','')+"\n")
  outfile.write(seq+"\n")

def parse_ortholog(uniprot_ids):
  m = dbClient.metaphors()
  for uniprot_id in uniprot_ids:
    outfile = open('Fasta/Ortholog_'+uniprot_id+'.fa','w')
    protid    = m.get_metaid(uniprot_id)
    orthologs = m.get_orthologs(protid)
    write_seq_to_file(m, '10090-'+uniprot_id, protid, outfile)
    for taxid, odata in orthologs.iteritems():
      for metaid, extid, CS, EL, noTrees, dbInfo, coOrthologs in odata:
        write_seq_to_file(m, taxid, metaid, outfile)
    outfile.close()
    print "Finished writing ortholog file for: %s" % uniprot_id
    
def parse_structure(uniprot_data):
  count_files = 0
  for uniprot_id in uniprot_data.keys():
    if 'pdbs' in uniprot_data[uniprot_id].keys():
      count_files += 1
      outfile = open('Structure/PDBcodes_'+uniprot_id+'.txt','w')
      pdbs = "\n".join(list(set(uniprot_data[uniprot_id]['pdbs'])))
      outfile.write(pdbs+"\n")
      outfile.close()
  print "Finished writing %i files for PDB codes" % count_files

def main():
  file_rawdata    = "data/MS_ISG15_Raw.tsv"
  MS_dict         = read_MS_rawdata(file_rawdata)
  all_uniprot_ids = sorted(MS_dict.keys())
  processed_ids   = [f.rsplit('_')[1].rsplit('.')[0] for f in glob.glob('Fasta/*.fa')]
  uniprot_ids     = sorted(list(set(all_uniprot_ids).difference(set(processed_ids))))
  print "All IDs: %i" % len(all_uniprot_ids)
  print "Processed IDs: %i" % len(processed_ids)
  print "Remaining IDs: %i" % len(uniprot_ids)
  uniprot_data = uniprot.batch_uniprot_metadata(uniprot_ids[0:150], 'cache')
  parse_structure(uniprot_data)
  parse_ortholog(uniprot_ids)

if __name__ == "__main__":
  main()
