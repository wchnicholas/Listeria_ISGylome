set ray_shadows, 0
bg_color white
set dash_width, 2
set dash_gap, 0.4
set sphere_scale, 0.3
set stick_radius=0.2

##########P06745 site 440##########
load PDB/2CVP.pdb
color palecyan, 2CVP and chain A
color lightpink, 2CVP and chain B
hide all
show cartoon, 2CVP
show sticks, 2CVP and chain A and resi 440 and (not name c+n+o)
show sticks, 2CVP and chain B and resi 520 and (not name c+n+o)
util.cnc all
set_view (\
     0.364689201,   -0.140973523,    0.920394301,\
    -0.094191827,   -0.988983333,   -0.114157312,\
     0.926350296,   -0.045062020,   -0.373950183,\
    -0.000039116,   -0.000004464, -206.221160889,\
    44.164138794,   -2.774272203,    4.705875874,\
   169.935684204,  242.505447388,  -20.000000000 )
ray; png graph/P06745_2CVP_440_zoomout.png

set_view (\
     0.364689201,   -0.140973523,    0.920394301,\
    -0.094191827,   -0.988983333,   -0.114157312,\
     0.926350296,   -0.045062020,   -0.373950183,\
    -0.000103791,   -0.000065967,  -58.157058716,\
    45.866786957,  -10.353581429,   17.994838715,\
    39.811561584,   76.487945557,  -20.000000000 )
distance dist1, /2CVP//A/LYS`440/NZ, /2CVP//B/GLN`520/OE1
show dashes, dist1; color black, dist1
hide label
ray; png graph/P06745_2CVP_440_zoomin.png

##########99KQ4 site 19##########
load PDB/2H3B.pdb
color palecyan, 2H3B and chain A
color lightpink, 2H3B and chain B
hide all
show cartoon, 2H3B
show sticks, 2H3B and chain A and resi 19 and (not name c+n+o)
show sticks, 2H3B and chain B and resi 246 and (not name c+n+o)
util.cnc all
set_view (\
    -0.035829719,   -0.114448622,    0.992782712,\
    -0.582546532,   -0.804786026,   -0.113801688,\
     0.812000930,   -0.582419753,   -0.037834216,\
    -0.000180006,    0.000116722, -283.753173828,\
    15.137696266,   -2.587425709,   23.133409500,\
   249.906127930,  317.616851807,  -20.000000000 )
ray; png graph/Q99KQ4_2H3B_19_zoomout.png

set_view (\
    -0.035829719,   -0.114448622,    0.992782712,\
    -0.582546532,   -0.804786026,   -0.113801688,\
     0.812000930,   -0.582419753,   -0.037834216,\
    -0.000204808,    0.000268127,  -65.581108093,\
     0.634252787,   14.864079475,   32.002319336,\
    53.551879883,   77.632408142,  -20.000000000 )
distance dist2, /2H3B//A/LYS`19/NZ, /2H3B//B/GLU`246/OE1 
show dashes, dist2; color black, dist2
hide label
ray; png graph/Q99KQ4_2H3B_19_zoomin.png

##########Q9JII6 site 23, 127, 157##########
load PDB/4GAC.pdb
color palecyan, 4GAC and chain A
color lightpink, 4GAC and chain B
hide all
show cartoon, 4GAC
show sticks, 4GAC and chain A and resi 23+127+157 and (not name c+n+o)
show sticks, 4GAC and chain B and resi 73 and (not name c+n+o)
util.cnc all
set_view (\
    -0.253090590,   -0.954960644,   -0.154876038,\
    -0.412045956,    0.251252562,   -0.875828385,\
     0.875289023,   -0.157851338,   -0.457081974,\
    -0.001620397,   -0.000098541, -198.257675171,\
   -22.753334045,  -19.731040955,   42.997711182,\
   168.064605713,  228.467010498,  -20.000000000 )
ray; png graph/Q9JII6_4GAC_19_zoomout.png

set_view (\
    -0.467309296,    0.679821014,    0.565209389,\
    -0.397012562,   -0.732588232,    0.552884400,\
     0.789921463,    0.033971652,    0.612245083,\
    -0.000010014,    0.000023462,  -43.181404114,\
   -16.505619049,   -3.633612156,   51.038932800,\
    22.331104279,   64.031463623,  -20.000000000 )
distance dist3, /4GAC//B/GLU`73/OE1, /4GAC//A/LYS`157/NZ
show dashes, dist3; color black, dist3
hide label
ray; png graph/Q9JII6_4GAC_19_zoomin_1.png

set_view (\
    -0.223454699,   -0.973553658,   -0.047525968,\
    -0.930024683,    0.227556303,   -0.288547128,\
     0.291723222,   -0.020279607,   -0.956273377,\
    -0.000574247,   -0.000046074,  -85.277778625,\
   -26.746717453,   -1.614451885,   20.694208145,\
    66.925224304,  103.696380615,  -20.000000000 )
util.cnc all
ray; png graph/Q9JII6_4GAC_19_zoomin_2.png

##########P09411 site 216##########
load PDB/4O3F.pdb
color palecyan, 4O3F and chain A
hide all
show cartoon, 4O3F
show sticks, 4O3F and chain A and resi 216 and (not name c+n+o)
util.cnc all
set_view (\
    -0.775418758,   -0.539348423,    0.328371584,\
     0.068737738,    0.444848984,    0.892955005,\
    -0.627688646,    0.714981973,   -0.307862222,\
    -0.000448957,    0.000493318, -200.742340088,\
     0.818125963,   -5.851812840,  -27.030700684,\
   175.940200806,  225.536239624,  -20.000000000 )
ray; png graph/P09411_4O3F_216_zoomout.png

########Q9JLN9 site 2066###########
load PDB/5H64.pdb
color palecyan, 5H64 and chain A
color lightpink, 5H64 and chain B
color grey80, 5H64 and chain C
hide all
show surface, 5H64
color orange, 5H64 and chain A and resi 2066

set_view (\
    -0.986583233,   -0.035768263,    0.159303188,\
    -0.158577412,   -0.022308268,   -0.987092316,\
     0.038862579,   -0.999111354,    0.016333725,\
    -0.000546217,   -0.000411021, -628.584106445,\
   195.942138672,  191.800292969,  199.824691772,\
   468.538085938,  788.581481934,  -20.000000000 )
ray; png graph/Q9JLN9_5H64_2066_zoomout.png

set_view (\
    -0.511903822,    0.020463064,   -0.858798623,\
     0.853934228,    0.120952278,   -0.506124377,\
     0.093520902,   -0.992445707,   -0.079389259,\
     0.000144018,    0.000433832, -435.979248047,\
   147.987609863,  167.016204834,  194.064910889,\
   353.127410889,  518.851440430,  -20.000000000 )
color orange, 5H64 and chain A and resi 2066 and (not name c+n+o)
ray; png graph/Q9JLN9_5H64_2066_zoomout_v2.png

set_view (\
    -0.741116345,   -0.106170714,   -0.662929714,\
     0.666839600,   -0.230982319,   -0.708495557,\
    -0.077898957,   -0.967146099,    0.241982520,\
     0.000259659,    0.000773847,  -89.534317017,\
   164.959518433,  155.562545776,  215.644134521,\
    40.859760284,  138.211639404,  -20.000000000 )
hide all
color palecyan, 5H64 and chain A
show cartoon, 5H64
show sticks, 5H64 and chain A and resi 2066 and (not name c+n+o)
util.cnc all
ray; png graph/Q9JLN9_5H64_2066_zoomin.png

########P51150 site 126#########
load PDB/1VG8.pdb
color palecyan, 1VG8 and chain A
hide all
show cartoon, 1VG8 and chain A
show sticks, 1VG8 and chain A and resi 1126 and (not name c+n+o)
show sticks, 1VG8 and resi 1400 and chain A
color orange, 1VG8 and resi 1400 and chain A
util.cnc all

set_view (\
    -0.652116895,    0.243209183,    0.718046188,\
    -0.499857873,    0.574169695,   -0.648435771,\
    -0.569984734,   -0.781777561,   -0.252857298,\
     0.000107244,    0.000117648, -164.714538574,\
     4.830338478,   -8.733734131,   33.718341827,\
   114.396369934,  215.033309937,  -20.000000000 )
ray; png graph/P51150_1VG8_126_zoomout.png

set_view (\
    -0.652116895,    0.243209183,    0.718046188,\
    -0.499857873,    0.574169695,   -0.648435771,\
    -0.569984734,   -0.781777561,   -0.252857298,\
     0.000112500,    0.000098573,  -56.371944427,\
    10.056315422,   -3.635836124,   24.903541565,\
    42.653785706,   70.089607239,  -20.000000000 )
distance dist4, /1VG8//A/LYS`1126/NZ, /1VG8//A/GNP`1400/O4'
show dashes, dist4; color black, dist4
hide label
ray; png graph/P51150_1VG8_126_zoomin.png
