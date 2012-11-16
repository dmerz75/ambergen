#!/usr/bin/env python
import os
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

my_dir = os.path.abspath(os.path.dirname(__file__))

wallclock=[]
cputime  =[]
memory   =[]
for path in glob(os.path.join(my_dir,'*/*-run.log*')):
    print path
    o=open(path,'r')
    for line in o.readlines()[-2:-1]:
        r,s,t,u,v,w,x,y,z=line.split(' ')
        wallclock.append(s)
        cputime.append(v)
        memory.append(y)
    o.close()

for item in wallclock:
    float(item)
wallclock.sort()
data = np.array(wallclock)
x=np.linspace(1,len(data),len(data))

# PLOT
fig=plt.figure()
plt.clf()
ax=fig.add_subplot(111)
ax.plot(x,data)

plt.draw()
plt.show()
fig.savefig('wt.png')
fig.savefig('wt.eps')
