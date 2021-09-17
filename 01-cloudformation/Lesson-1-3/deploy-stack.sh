#!/usr/bin/env sh

set -x pipefail

# Ensure we have awscli installed; 
which aws

# Set the regions
REGIONS=`(cat regions.json | jq -r '.Regions[].RegionName')`

echo $REGIONS

# Loop over the REGIONS var and create the bucket in each region
for REGION in $REGIONS 
do 
  aws cloudformation deploy --stack-name mike-uni-training --template-file s3.yaml --region $REGION
done