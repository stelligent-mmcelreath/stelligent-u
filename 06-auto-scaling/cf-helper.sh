#!/usr/bin/env sh

# set -euo pipefail
set -xe

# A script for creating / updating / deleting CloudFormation tempaltes 

# Check to see if AWS cli is installed 
which aws

# Variables
STACK_NAME=$1
OPERATION=$2 # delete or deploy 
TEMPLATE_FILE=${3:-default}



CF_EXISTS() {
    # Check to see if $STACK_NAME exists
    aws cloudformation describe-stacks --stack-name $STACK_NAME
}


CF_DEPLOY() {
    # Create or Update Cloudformation STACK_NAME with provided TEMPLATE_FILE
    aws cloudformation deploy --stack-name $STACK_NAME --template-file $TEMPLATE_FILE
}

CF_DELETE() {
    # Delete the cloudformation stack because the delete flag was passed.
    aws cloudformation delete-stack --stack-name $STACK_NAME
}
  
  

# Check for all required parameters then decipher what other params were passed in.

if [ -z "$1" ] || [ -z "$2" ]; then 
    echo "STACK_NAME  is required!"
    exit 1
elif
    [ $OPERATION == "deploy" ]; then
    if CF_EXISTS; then
        echo -n "Stack exists, updating stack $STACK_NAME!"
        CF_DEPLOY
    else 
        echo -n "Stack does not exist, creating $STACK_NAME!"
        CF_DEPLOY
    fi
elif 
    [ $OPERATION == "delete" ]; then
    echo "Deleting Stack $STACK_NAME"
    CF_DELETE
else
    echo -n "Somethings wrong check your parameters and try again!"
fi
