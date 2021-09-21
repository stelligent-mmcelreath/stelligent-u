#!/usr/bin/env sh
set -x pipefail

# Make sure AWS CLI is instlled 
which aws


STACK_NAME=ec2-training-mike

# Create stack and wait for resource to be created. 
 aws cloudformation deploy --stack-name $STACK_NAME --template-file ec2.yaml && aws cloudformation wait stack-create-complete --stack-name $STACK_NAME