#!/usr/bin/env python
import MDAnalysis
import MDAnalysis.analysis.hbonds
import MDAnalysis.analysis.distances
from sys import argv
import numpy as np
import pickle
import os,sys

script,stri,strjob = argv

#______________universe______________________________________________________
u = MDAnalysis.Universe('../../xxenvironxx/00.prmtop','mdtraj.mdcrd',
                        permissive=True)
h = MDAnalysis.analysis.hbonds.HydrogenBondAnalysis(u,'protein','protein',
                                                distance=4.0, angle=140.0)
results = h.run()

#______________h.timeseries__________________________________________________
pickle.dump(h.timeseries,open('%s-hb.pkl.%s' % (stri,strjob),'w'))

f = open('%s-hlist.dat.%s' % (stri,strjob),'w')
for n in range(0,len(h.timeseries)):
    for bond in h.timeseries[n]:
        for val in bond:
            try:
                f.write(val+'   \t')
            except:
                f.write(str(val)+'   \t')
        f.write('\n')
    f.write('# '+str(n)+' ')
    f.write(str(len(h.timeseries[n])))
    f.write('\n')
    f.write('\n')
f.close()
#______________rgyr__________________________________________________________
acc=[]
listl=[]
rg=[]

def cyc(ca1,ca2):
    for ts in u.trajectory:
        r1 = ca2.coordinates() - ca1.coordinates()
        d1 = np.linalg.norm(r1)
        acc.append(d1)

def calcd(i,ca):
    ca1 = u.selectAtoms("resid %d and name CA" % i)
    ca2 = u.selectAtoms("resid %d and name CA" % ca)
    cyc(ca1,ca2)

for i in range(1,5):
    ca = 11-i
    calcd(i,ca)
    listl.append(acc)
    acc=[]

def rgyr(bb):
    for ts in u.trajectory:
        rgyr = bb.radiusOfGyration()
        rg.append(rgyr)

bb = u.selectAtoms('protein and backbone')   # a selection (a AtomGroup)
rgyr(bb)
listl.append(rg)

dd = np.array(listl)
dd = np.transpose(dd)
np.savetxt('%s-rgyr.dat.%s' % (stri,strjob),dd,fmt='%.14f')
