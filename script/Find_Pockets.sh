#!/bin/bash
for f in PDB/*.pdb
do
echo $f
/Users/wchnicholas/Bioinformatics/fpocket2/bin/fpocket -f $f
done
