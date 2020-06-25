find . -name '.DS_Store' -type f -ls -delete
aws s3 sync /Users/nakamurasatoshi/git/d_sat/sat_images/docs s3://sat-iiif