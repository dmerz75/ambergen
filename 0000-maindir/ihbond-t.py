#!/usr/bin/env python
import MDAnalysis
import MDAnalysis.analysis.hbonds
import matplotlib.pyplot as plt
from sys import argv
from glob import glob
import numpy as np
import pickle
import sys,os,re

my_dir = os.path.abspath(os.path.dirname(__file__))

acc=[]
for path in glob(os.path.join(my_dir,'xxnumxx.*/*-hb.pkl')):
    print path
    sample_i = pickle.load(open(path,'rb'))
    acc.append(sample_i)
    if len(acc)==250:
        break

def residue_index(label):
    return int(re.sub("[^0-9]","",label))

def charac_bond2(trajectory, distance_target):
    acc_count_frames = []
    for frame in trajectory:
        acc_count = 0
        for bond in frame:
            distance = residue_index(bond[2]) - residue_index(bond[3])
            if distance == distance_target:
               acc_count += 1
        acc_count_frames.append(acc_count)
    return acc_count_frames


b_data = np.array([[charac_bond2(traj_i, n) for traj_i in acc]
     for n in [3,4,5]])

trj  = str(len(acc))
trjl = len(acc[0])

# matplotlib
frames = np.linspace(13,33,len(acc[0]))
plt.plot(frames,b_data.mean(axis=1)[0],'r-',label="i->i+3")
#plt.plot(frames,b_data[0][0],'r.',label="i->i+3")
plt.plot(frames,b_data.mean(axis=1)[1],'k-',label="i->i+4")
plt.plot(frames,b_data.mean(axis=1)[2],'g-',label="i->i+5")
plt.xlabel('end-to-end distance (A)')
plt.ylabel('Average H-bond count')
plt.title('Deca-alanine Structure: NAMD/Charmm22 %strj' % trj)
plt.legend()
plt.axis([9.9,35.1,-.1,6.4])

plt.draw()
plt.savefig('xxnumxx-hbs.eps')
plt.savefig('xxnumxx-hbs.png')
