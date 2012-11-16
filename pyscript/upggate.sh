#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/namdgen/103.da.c130/
DESTDIR=dmerz3@ggate.chemistry.gatech.edu:/nethome/dmerz3/Documents/valiant/ggate/01.da/

#rsync -avh $SOURCEDIR $DESTDIR
scp -r $SOURCEDIR $DESTDIR
