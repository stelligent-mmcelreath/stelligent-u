#!/usr/bin/env python3

import boto3
import json
import sys
import os.path


        
def stack_exists(Client, Stack_Name, Template_File): 
    # Check to see if that stack exists in the region
    try:
        if Client.describe_stacks(
            StackName=Stack_Name):
            return True
    except:
            return False

def stack_update(Client, Stack_Name, Template_File):
    print("Updating {} stack in region {}".format(Stack_Name, Client.meta.region_name))
    response = Client.update_stack(
        StackName = Stack_Name,
        TemplateBody = Template_File,
        Parameters = [{
                'ParameterKey': 'BucketNameParam',
                'ParameterValue': 'mmcelreath-cdk-update' 
            }]
    )
    print(response)



def stack_create(Client, Stack_Name, Template_File):
    print("Creating {} stack in region {}".format(Stack_Name, Client.meta.region_name))
    response = Client.create_stack(
        StackName = Stack_Name,
        TemplateBody = Template_File,
        Parameters = [{
                'ParameterKey': 'BucketNameParam',
                'ParameterValue': 'mmcelreath-cdk' 
            }]
    )
    print(response)

def stack_delete(Client, Stack_Name):
    print("Deleting {} stack in region {}".format(Stack_Name, Client.meta.region_name))
    response = Client.delete_stack(
		StackName=Stack_Name
	)
    print(response)




def main():
    
    # Create the template body object since we'll need it everywhere.
    Template_File = open("s3.yaml", "r").read()
    # Read the regions file and delcare an object
    Regions_File = open("regions.json")
    Data = json.load(Regions_File)


    # Parse out the regions and create a Client for each region. 
    for REGIONS in Data["Regions"]:
        Client = boto3.client('cloudformation', region_name=REGIONS["RegionName"])
        try:
            if len(sys.argv[3]) >3 and sys.argv[3] == "delete":
                stack_exists(Client, Stack_Name, Template_File)
                stack_delete(Client, Stack_Name)
        except:
            if stack_exists(Client, Stack_Name, Template_File):
               stack_update(Client, Stack_Name, Template_File)
            else:
               stack_create(Client, Stack_Name, Template_File)
        
        # stack_exists(Client, Stack_Name, Template_File)

    
             
    Regions_File.close()
    




if __name__ == "__main__":
    # add some args here so we can sataisfy running only a single shell command
    Stack_Name = sys.argv[1] if len(sys.argv) >1 else 'null'
    Template_File = sys.argv[2] if len(sys.argv) >2 else 'null'

    print(Template_File)
    print(Stack_Name)

    if len(sys.argv[1:]) >=3 and sys.argv[3] == "delete":
        print("Deleting stack")
        main()
    elif len(sys.argv[1:]) ==2 and os.path.isfile(Template_File):
        print("Creating stack if not exists, else updating")
        main()
    elif len(sys.argv[1:]) <2:
        print("Missing arguments. \nUsage: ./cdk.py <stack-name> <template-yaml> <delete (optional)>")
        exit()
    else:
        print("Somethings went horribly wrong, read the manual and try again! \n (Perhaps your file or path is incorrect?)")


    