#!/usr/bin/python
import os
import sys
import glob
import uniprot
import numpy as np
import dssp_parser as dd
from prody import *
from Bio import pairwise2
from collections import defaultdict

def reading_ASA(file_asa):
  infile = open(file_asa,'r')
  dict_asa = {}
  for line in infile.xreadlines():
    if 'aa' in line: continue
    line = line.rstrip().rsplit("\t")
    aa  = line[0]
    asa = line[3]
    dict_asa[aa] = asa
  return dict_asa

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

def reading_dssp(file_dssp, dict_asa):
  dd_ob = dd.DSSPData()
  dd_ob.parseDSSP(file_dssp)
  dict_dssp = {}
  for resi, chain, aa, SA in zip(dd_ob.getResnums(), dd_ob.getChain(), dd_ob.getAAs(), dd_ob.getACC()):
    if resi == "": continue
    if aa not in ['E','D','R','K','H','Q','N','S','T','P','G','C','A','V','I','L','M','F','Y','W']: continue
    RSA = float(SA)/float(dict_asa[aa])
    dict_dssp[chain+'-'+resi] = {'SA':SA, 'RSA':RSA}
  return dict_dssp

def identify_position(uniprot_seq_aln, pdb_seq_aln, position, uniprot_id):
  uniprot_resi = 0
  pdb_resi     = 0
  for n in range(len(uniprot_seq_aln)):
    if pdb_seq_aln[n] != '-':
      pdb_resi += 1
    if uniprot_seq_aln[n] != '-':
      uniprot_resi += 1
      if uniprot_resi == position:
        if uniprot_seq_aln[n]!='K':
          print 'Target resi on uniprot is not a K (%s)' % uniprot_id
        if pdb_seq_aln[n]=='-':
          print 'Target resi on PDB is a gap (%s)' % uniprot_id
          return 'NA'
        elif pdb_seq_aln[n]!='K':
          print 'Target resi on PDB is not a K (%s)' % uniprot_id
          return 'NA'
        return pdb_resi, pdb_seq_aln[n]

def align_uniprot_PDB(uniprot_seq, atoms, chain_id):
  hv   = atoms.getHierView()[chain_id]
  pdb_seq  = hv.getSequence()
  alns = pairwise2.align.globalxx(uniprot_seq, pdb_seq)
  if len(alns) > 0: return alns[0]
  else: return 'NA'

def get_RSA_all_lys(atoms, dict_dssp, uniprot_id, PDB, outfile):
  Lys_atoms = atoms.select('resname LYS')
  if Lys_atoms == None: return 'NA'
  residueIDs = list(set([chain_id+'-'+str(resnum) for chain_id, resnum in zip(Lys_atoms.getChids(), Lys_atoms.getResnums())]))
  for residueID in residueIDs:
    if residueID not in dict_dssp.keys(): continue
    RSA = dict_dssp[residueID]['RSA']
    chain_id = residueID.rsplit('-')[0]
    resnum   = residueID.rsplit('-')[1]
    outfile.write("\t".join(map(str,['All', uniprot_id, resnum, PDB, chain_id, resnum, RSA]))+"\n")
 
def parse_uniprot_PDB(filename, MS_dict, dict_asa, outfile):
  uniprot_id   = filename.rsplit('_')[1].rsplit('.')[0]
  uniprot_data = uniprot.batch_uniprot_metadata([uniprot_id], 'cache')
  uniprot_seq  = uniprot_data[uniprot_id]['sequence']
  positions    = list(set(MS_dict[uniprot_id]['Position']))
  PDBs = [line.rstrip() for line in open(filename,'r').readlines()]
  for PDB in PDBs:
    file_PDB_zip = 'PDB/'+PDB+'.pdb.gz'
    file_PDB     = 'PDB/'+PDB+'.pdb'
    file_dssp    = 'dssp/'+PDB+'.dssp'
    fetchPDB(PDB)
    if len(glob.glob(PDB+'.pdb.gz'))==0: continue
    os.system('mv '+PDB+'.pdb.gz PDB/')
    os.system('gunzip -f '+file_PDB_zip)
    os.system('/usr/local/Cellar/dssp/2.1.0/bin/mkdssp '+file_PDB+' > '+file_dssp)
    dict_dssp = reading_dssp(file_dssp, dict_asa)
    atoms     = parsePDB(file_PDB)
    get_RSA_all_lys(atoms, dict_dssp, uniprot_id, PDB, outfile)
    chain_ids = sorted(list(set(atoms.getChids())))
    for chain_id in chain_ids:
      chain_atoms = atoms.select('chain '+chain_id)
      top_aln = align_uniprot_PDB(uniprot_seq, atoms, chain_id)
      if top_aln == 'NA': print "No alignment"; continue
      uniprot_seq_aln, pdb_seq_aln, score, begin, end = top_aln
      for position in positions:
        if position < int(begin): continue
        if position > int(end): continue
        pdb_resi, pdb_aa = identify_position(uniprot_seq_aln, pdb_seq_aln, position, uniprot_id)
        if pdb_resi == 'NA': continue
        pdb_resi  = sorted(list(set(chain_atoms.getResnums())))[pdb_resi-1]
        residueID = chain_id+'-'+str(pdb_resi)
        if residueID not in dict_dssp.keys(): continue
        RSA = dict_dssp[residueID]['RSA']
        outfile.write("\t".join(map(str,['ISG15', uniprot_id, position, PDB, chain_id, pdb_resi, RSA]))+"\n")

def main():
  file_RSA     = 'result/ISG15_Lys_RSA.tsv'
  file_rawdata = "data/MS_ISG15_Raw.tsv"
  MS_dict      = read_MS_rawdata(file_rawdata)
  filenames = glob.glob('Structure/PDBcodes*.txt')
  file_asa  = 'data/ASA.table'
  dict_asa  = reading_ASA(file_asa)
  outfile = open(file_RSA,'w')
  outfile.write("\t".join(['Type', 'UniProt_ID', 'position', 'PDB', 'PDB_chain', 'PDB_resi', 'RSA'])+"\n")
  for filename in filenames:
    parse_uniprot_PDB(filename, MS_dict, dict_asa, outfile)
  outfile.close()
  print "Output written in: %s" % file_RSA

if __name__ == "__main__":
  main()
