rsync -tCrvc --exclude-from=.deployexclude --inplace --del ./ $1
