#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/source105/
DESTDIR=dmerz3@tg-steele.purdue.teragrid.org:/scratch/scratch96/d/dmerz3/valiant/steele/01.da/

#rsync -avh $SOURCEDIR $DESTDIR
scp -r $SOURCEDIR $DESTDIR
