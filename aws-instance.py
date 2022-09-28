import os
import sys
import boto3
from botocore.exceptions import ClientError

from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv('aws_access_key_id')
SECRET_KEY = os.getenv('aws_secret_access_key')
INSTANCE_ID = os.getenv('aws_instance_id')
REGION = os.getenv('aws_region')

action = sys.argv[1].upper()

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION
)

if action == 'START':
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
        print(f'Instance Starting')
    except ClientError as e:
        print(e)
elif action == 'STOP':
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[INSTANCE_ID], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
        print(f'Instance stopping')
    except ClientError as e:
        print(e)
elif action == 'STATUS':
     # Get status of instance
    try:
        response = ec2.describe_instances(InstanceIds=[INSTANCE_ID], DryRun=False)
        status = response['Reservations'][0]['Instances'][0]['State']['Name']
        print(f'Instance is currently: {status}')
    except ClientError as e:
        print(e)
else:
    print(f'{action} is not a valid command. Try START, STOP, or STATUS')