#!/usr/bin/env python
import sys, os

JOBID = os.environ['PBS_JOBID']
JOBID1 = JOBID.split('.')[0]

howmany = xxhowmanyxx
for i in range(1, howmany+1):
    os.system('${AMBERHOME}/bin/sander -O -i smd.in -o run.log -c 00.inpcrd -p \
              00.prmtop -r md_smd.rst -x mdtraj.mdcrd -v mdvel.mdvel')
    os.system("mv tef.dat %d-tef.dat.%s" % (i,JOBID1))
