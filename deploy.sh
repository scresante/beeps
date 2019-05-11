#!/bin/sh
if [ -z $1 ] ; then
    echo need arg; exit
fi
rsync -tCrvc --exclude-from=.deployexclude --inplace --del ./ $1
