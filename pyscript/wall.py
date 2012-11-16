#!/usr/bin/env python
import sys, os, glob
import os.path
from glob import glob
import fnmatch
import itertools
import pickle

my_dir = os.path.abspath(os.path.dirname(__file__))

assembly={}
def assemble(cd,wc):
    if cd not in assembly:
        assembly[cd]=0
    assembly[cd]+=1
assembly2={}
def assemble2(cd,wc):
    assembly2[cd]=wc

acc=[]
for root, dirnames, filenames in os.walk(my_dir):
    for filename in fnmatch.filter(filenames,'*-run.log*'):
        jobs=os.path.join(root,filename)
        dir='/'.join(jobs.split('/')[0:-1])
        a=(jobs.split('/')[-2]).split('.')[0]
        if (a=='03') or (a=='04') or (a=='05'):
            o=open(jobs,'r')
            for line in o.readlines()[-2:-1]:
            wc=line.split(' ')[1]
        o.close()
            c=(jobs.split('/')[-3]).split('.')[1]
            d=(jobs.split('/')[-2]).split('.')[0]
            cd=c+d
            zz=cd+' '+str(wc)
            acc.append(zz)
        assemble(cd,wc)
        assemble2(cd,wc)
print len(acc)
print 'tis the length of acc'

result={}
def count():
    for cond in acc:
        if cond not in result:
            result[cond]=0
        result[cond]+=1
count()

vac03=[]
vac04=[]
vac05=[]
imp03=[]
imp04=[]
imp05=[]
exp03=[]
exp04=[]
exp05=[]
for key in assembly:
    print key + '  ' + str(assembly[key])
for val in acc:
    valc=val.split(' ')[0]
    valn=val.split(' ')[1]
    if valc=='vac03':
       vac03.append(valn)
    elif valc=='vac04':
        vac04.append(valn)
    elif valc=='vac05':
        vac05.append(valn)
    elif valc=='imp03':
        imp03.append(valn)
    elif valc=='imp04':
        imp04.append(valn)
    elif valc=='imp05':
        imp05.append(valn)
    elif valc=='exp03':
        exp03.append(valn)
    elif valc=='exp04':
        exp04.append(valn)
    elif valc=='exp05':
        exp05.append(valn)
confd={}
confd['vac03']=vac03
confd['vac04']=vac04
confd['vac05']=vac05
confd['imp03']=imp03
confd['imp04']=imp04
confd['imp05']=imp05
confd['exp03']=exp03
confd['exp04']=exp04
confd['exp05']=exp05
pickle.dump(confd,open('time345.pkl','w'))
