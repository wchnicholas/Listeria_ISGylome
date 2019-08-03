#!/usr/bin/python
import os
import sys
import glob
from prody import *

def reading_resi(filename):
  ID = filename.rsplit('/')[1].rsplit('_out')[0]
  atoms     = parsePDB(filename)
  chain_ids = atoms.getChids()
  resnums   = atoms.getResnums()
  pocket_residues = []
  for chain_id, resnum in zip(chain_ids, resnums):
    resi_id = "-".join(map(str,[ID, chain_id, resnum]))
    pocket_residues.append(resi_id)
  return list(set(pocket_residues))

def writing_pockets(all_pocket_residues, file_pocket_resi):
  print "Writing: %s" % file_pocket_resi
  outfile = open(file_pocket_resi,'w')
  outfile.write("\t".join(['PDB','PDB_chain','PDB_resi'])+"\n")
  for resi in all_pocket_residues:
    outfile.write(resi.replace('-',"\t")+"\n")
  outfile.close()

def main():
  file_pocket_resi = 'result/ISG15_pockets.tsv'
  filenames = glob.glob('PDB/*_out/pockets/*_atm.pdb')
  all_pocket_residues = []
  for filename in filenames:
    pocket_residues = reading_resi(filename)
    all_pocket_residues+=pocket_residues
  writing_pockets(all_pocket_residues, file_pocket_resi)

if __name__ == "__main__":
  main()
