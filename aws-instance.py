import os
import sys
import time
from typing import Any
import boto3
from botocore.exceptions import ClientError

from dotenv import load_dotenv

def get_instance_status(ec2 , INSTANCE_ID: str):
    response = ec2.describe_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
    instance = response['Reservations'][0]['Instances'][0]
    status = instance['State']['Name']
    publicDNS = instance['PublicDnsName']
    info = {'status': status, 'publicDNS':publicDNS}
    return instance, info




load_dotenv()

ACCESS_KEY = os.getenv('aws_access_key_id')
SECRET_KEY = os.getenv('aws_secret_access_key')
INSTANCE_ID = os.getenv('aws_instance_id')
REGION = os.getenv('aws_region')

TIMEOUT = 60 * 5 # 3 minutes

action = sys.argv[1].upper()
# action = 'start'.upper()

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

if action == 'START':
    # Do a dryrun first to verify permissions
    try:
        response = ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
        print(response)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise Exception('')

    # Dry run succeeded, run start_instances without dryrun
    start_time = time.perf_counter()
    curr_time = time.perf_counter()

    try:
        response = ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
        print(f'Instance is starting...')
        
        while curr_time - start_time < TIMEOUT:
            curr_time = time.perf_counter()
            elapsed_time = round(curr_time - start_time)
            time.sleep(5)
            instance, info = get_instance_status(ec2, INSTANCE_ID)
            status = info["status"]
            print(f'{elapsed_time} secs - Instance is currently: {status}')
            if status == 'running':
                print(f'Instance has started successfully at {info["publicDNS"]}')
                break
        else:
            raise Exception(f'Timeout of {TIMEOUT} seconds has been reached and action has failed please try again.')


    except ClientError as e:
        print(e)
elif action == 'STOP':
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise Exception('')

    # Dry run succeeded, call stop_instances without dryrun

    start_time = time.perf_counter()
    curr_time = time.perf_counter()

    try:
        response = ec2.stop_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
        print(f'Instance is stopping...')
        
        while curr_time - start_time < TIMEOUT:
            curr_time = time.perf_counter()
            elapsed_time = round(curr_time - start_time)
            time.sleep(5)
            instance, info = get_instance_status(ec2, INSTANCE_ID)
            status = info["status"]
            print(f'{elapsed_time} secs - Instance is currently: {status}')
            if status == 'stopped':
                print(f'Instance has stopped successfully')
                break
        else:
            raise Exception(f'Timeout of {TIMEOUT} seconds has been reached and action has failed please try again.')
    except ClientError as e:
        print(e)

elif action == 'STATUS':
     # Get status of instance
    try:
        instance, info = get_instance_status(ec2, INSTANCE_ID)
        print(f'Instance is currently: {info["status"]}')
        if info['publicDNS']:
            print(f'PublicDNS: {info["publicDNS"]}')
    except ClientError as e:
        print(e)
else:
    print(f'{action} is not a valid command. Try START, STOP, or STATUS')