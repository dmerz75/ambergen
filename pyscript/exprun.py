#!/usr/bin/env python
import sys, os, glob
import os.path
from glob import glob
import fnmatch
import itertools

my_dir = os.path.abspath(os.path.dirname(__file__))

acc=[]
for root, dirnames, filenames in os.walk(my_dir):
    for filename in fnmatch.filter(filenames,'*-expavg.py'):
        jobs=os.path.join(root,filename)
        print jobs
        dir='/'.join(jobs.split('/')[0:-1])
        os.chdir(dir)
        os.system('python ' + '%s' % jobs)
