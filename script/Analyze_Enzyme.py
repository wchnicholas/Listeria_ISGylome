#!/usr/bin/python
import os
import sys
import glob
from collections import defaultdict

def reading_raw(file_raw):
  infile  = open(file_raw, 'r')
  MS_dict = defaultdict(dict)
  for line in infile.xreadlines():
    if 'C: Cluster' in line: continue
    line = line.rstrip().rsplit("\t")
    clusterid = line[0]
    proteinid = line[1]
    site      = line[2]
    describe  = line[3]
    if '_' in proteinid:
      print "Ignored protein ID: %s" % proteinid
      continue
    else:
      uniprotid = proteinid
      if uniprotid in MS_dict.keys():
        MS_dict[uniprotid]['sites'].append(site)
        if clusterid not in MS_dict[uniprotid]['clusters']:
          MS_dict[uniprotid]['clusters'].append(clusterid)
      else:
        MS_dict[uniprotid] = {'clusters':[clusterid], 'sites':[site],
                              'describe':describe}
  infile.close()
  return MS_dict

def reading_rsa(file_rsa):
  infile = open(file_rsa, 'r')
  rsa_dict = {}
  for line in infile.xreadlines():
    line  = line.rstrip().rsplit("\t")
    Type  = line[0]
    ID    = line[1]
    site  = line[2]
    PDB   = line[3]
    chain = line[4]
    resi  = line[5]
    rsa   = line[6]
    PDB_site_identifier = '-'.join([PDB,chain,resi])
    if Type != 'ISG15': continue
    if ID not in rsa_dict.keys():
      rsa_dict[ID] = {site:{PDB_site_identifier:rsa}}
    else:
      if site not in rsa_dict[ID].keys():
        rsa_dict[ID][site] = {PDB_site_identifier:rsa}
      else:
        rsa_dict[ID][site][PDB_site_identifier] = rsa
  infile.close()
  print 'Analyzing %i sites from PDB' % len(rsa_dict.keys())
  return rsa_dict

def reading_con(file_con):
  infile = open(file_con, 'r')
  con_dict = {}
  for line in infile.xreadlines():
    line  = line.rstrip().rsplit("\t")
    Type  = line[0]
    ID    = line[1]
    site  = line[2]
    con_K = line[6]
    if Type != 'ISG15': continue
    if ID not in con_dict.keys():
      con_dict[ID] = {site:con_K}
    else:
      con_dict[ID][site] = con_K
  return con_dict

def reading_poc(file_poc):
  infile = open(file_poc, 'r')
  poc_list = []
  for line in infile.xreadlines():
    line  = line.rstrip().rsplit("\t")
    PDB   = line[0]
    chain = line[1]
    resi  = line[2]
    PDB_site_identifier = '-'.join([PDB,chain,resi])
    poc_list.append(PDB_site_identifier)
  infile.close()
  return poc_list
  
def selecting_sites(MS_dict, rsa_dict, con_dict, poc_list, file_out):
  print "Writing: %s" % file_out
  outfile = open(file_out, 'w')
  outfile.write("\t".join(['UniProt_ID','position','RSA','PDB_identifier','Lys_Conservation','pocket','description'])+"\n")
  for ID in MS_dict.keys():
    describe = MS_dict[ID]['describe']
    clusters = MS_dict[ID]['clusters']
    if 'cluster 1' not in clusters: continue
    #if 'ase' not in MS_dict[ID]['describe']: continue
    for site in sorted(MS_dict[ID]['sites'],key=lambda x:int(x)):
      if ID not in rsa_dict.keys(): continue
      if ID not in con_dict.keys(): continue
      if site not in rsa_dict[ID].keys(): continue
      if site not in con_dict[ID].keys(): continue
      for PDB_site_identifier in rsa_dict[ID][site].keys():
        rsa = float(rsa_dict[ID][site][PDB_site_identifier])
        con = float(con_dict[ID][site])
        poc = ''
        if PDB_site_identifier in poc_list: poc = 'yes'
        else: poc = 'no'
        outfile.write("\t".join(map(str,[ID, site, rsa, PDB_site_identifier, con, poc, describe]))+"\n")
  outfile.close()

def main():
  file_out = 'result/ISG15_sites_of_interest.tsv'
  file_raw = 'data/MS_ISG15_Raw.tsv'
  file_rsa = 'result/ISG15_Lys_RSA.tsv'
  file_con = 'result/ISG15_Lys_con.tsv'
  file_poc = 'result/ISG15_pockets.tsv'
  MS_dict  = reading_raw(file_raw)
  rsa_dict = reading_rsa(file_rsa)
  con_dict = reading_con(file_con)
  poc_list = reading_poc(file_poc)
  selecting_sites(MS_dict, rsa_dict, con_dict, poc_list, file_out)
  
if __name__ == "__main__":
  main()
