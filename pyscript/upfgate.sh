#!/bin/bash
# rsync ggate

SOURCEDIR=/home/dale/Documents/valiant/workgen/ambergen/amb105c.da.c130/
DESTDIR=dmerz3@fgate-fs.chemistry.gatech.edu:/nethome/dmerz3/Documents/valiant/fgate/01.da/

#rsync -avh $SOURCEDIR $DESTDIR
scp -r $SOURCEDIR $DESTDIR
