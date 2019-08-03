set ray_shadows, 0
bg_color white
set cartoon_side_chain_helper, on 
set transparency, 0.7

load PDB/1ubq.pdb
load PDB/1z2m.pdb
set_view (\
    -0.452616274,    0.839893043,    0.299524337,\
     0.772328377,    0.201353282,    0.602467716,\
     0.445697308,    0.504016578,   -0.739808977,\
     0.000042435,   -0.000075303, -130.229095459,\
    30.663301468,   29.466598511,   15.742151260,\
   104.886833191,  155.574508667,  -20.000000000 )
hide all
show cartoon, 1ubq
show sticks, 1ubq and resi 6+29 and (not name c+n+o)
show surface, 1ubq
color white, 1ubq
color purple, 1ubq and resi 6+29
util.cnc 1ubq and resi 6+29
ray; png graph/highlight_lys_ubiquitin.png

set_view (\
    -0.345525533,    0.294297636,   -0.891065359,\
    -0.205058813,   -0.950281739,   -0.234342009,\
    -0.915729403,    0.101750530,    0.388695776,\
     0.000073418,   -0.000050876, -201.019592285,\
    26.141016006,   31.445901871,    9.966073990,\
   147.238143921,  254.805160522,  -20.000000000 )
hide all
show cartoon, 1z2m
show sticks, 1z2m and resi 8+35 and (not name c+n+o)
show surface, 1z2m
color white, 1z2m
color purple, 1z2m and resi 8+35
util.cnc 1z2m and resi 8+35
ray; png graph/highlight_lys_ISG15.png
