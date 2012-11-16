#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/source105/

#/home/dale/Documents/valiant/steele/01.da/100ss/100sa.da.c130/01.vac
DESTDIR=/home/dale/Documents/valiant/steele/01.da/105.da.c130/

#DESTDIR=/mnt/hgfs/debian2shared/namd/

#scp -r $SOURCEDIR $DESTDIR
rsync -avh --include='*/' --include='*-npy.py' --include='*-dualplot.py' --include='*-expavg.py' --exclude='*' $SOURCEDIR $DESTDIR
