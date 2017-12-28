#!/usr/bin/env python
from __future__ import print_function
import argparse
import boto3
import logging
import re

RESPONSE_INDEX = 0

def describe_addresses(input_ip_address, ec2_region):
    """This function takes the input IP address and returns the information relevant to
    the main function for further processing"""
    describe_client = boto3.client('ec2',region_name=ec2_region)

    describe_response = describe_client.describe_addresses(PublicIps=[input_ip_address])

    return describe_response

def is_already_attached_to_instance(instance_id, ip_address_attachment):
    #will check to see if the instance ID already has the EIP assigned to it
    if instance_id is not ip_address_attachment['Addresses'][RESPONSE_INDEX]['InstanceId']:
        print ("Input Instance ID: " + instance_id + "\nCurrently attached Instance: " + 
                ip_address_attachment['Addresses'][RESPONSE_INDEX]['InstanceId'])
        return True
    else:
        return False

def reattach_eip(instance_id, region, describe_eip):
    reattach_client = boto3.client('ec2', region_name=region)

    eip_association = describe_eip['Addresses'][RESPONSE_INDEX]['AssociationId']
    eip_allocation = describe_eip['Addresses'][RESPONSE_INDEX]['AllocationId']

    detach_response = reattach_client.disassociate_address(AssociationId=eip_association)
    reattach_response = reattach_client.associate_address(AllocationId=eip_allocation, InstanceId=instance_id)
    return reattach_response

def main():
    """main function that grabs inputs and executes describes EIP and reattaches to new instance"""
    #main function that will define all actions run in the account
    parser = argparse.ArgumentParser(description='This tool takes an input'
                        ' Elastic IP and reassigns it to a new instance.')
    parser.add_argument('ip_address',action='store', type=str, help='provide the EIP (elastic IP) to'
                        ' re-assign')
    parser.add_argument('-i', action='store', type=str, help='instance-id to attach the ip to.')
    parser.add_argument('-r', action='store', type=str, help='if you want to pass a region that is not'
                        ' the default region, add the specific region here')
    args = parser.parse_args()

    if args.r is None:
        # sets the region to the session default if the -r flag is not set
        args.r = boto3.Session().region_name

    if args.ip_address is not None:
        if args.i is not None:
            ip_address_response = describe_addresses(args.ip_address, args.r)
    
    print (is_already_attached_to_instance(args.i, ip_address_response))

    if is_already_attached_to_instance(args.i, ip_address_response):
        is_reattached = reattach_eip(args.i, args.r, ip_address_response)
    else:
        print ("already attached to the input instance")

    print (is_reattached)

if __name__ == "__main__":
    main()