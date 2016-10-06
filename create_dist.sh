#!/bin/sh

# Create the latest dist archive for the projects and copy them at the right place
# for deployment

ERMR_PWD=${PWD}  
ERMR_VERSION="1.1"

# Create and copy the latest archive for indigo code

cd ${ERMR_PWD}/indigo
python setup.py sdist --formats=gztar
cp dist/indigo-${ERMR_VERSION}.tar.gz ${ERMR_PWD}/ermr-deploy/files

# Create and copy the latest archive for indigo-web code

cd ${ERMR_PWD}/indigo-web
python setup.py sdist --formats=gztar
cp dist/indigo-web-${ERMR_VERSION}.tar.gz ${ERMR_PWD}/ermr-deploy/files
