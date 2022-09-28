# AWS instance utility

## Summary

A Python script that will control the state of an AWS instance remotely.

### Use cases

The following actions are currently implemented.

START - Start the AWS instance

STOP - Stop the AWS instance

STATUS - Return the current state of the AWS instance

## Requirements

Install necessary packages

    python3 -m pip install -r requirements.txt

The script requires a .env file with the following variables in the root directory. This controls which instance you want to control and requires your sensitive aws keys to work.

    aws_access_key_id=ACCESS_KEY
    aws_secret_access_key=SECRET_KEY
    aws_instance_id=INSTANCE_ID
    aws_region=REGION

## Commands

The following actions are currently implemented.

START - Start the AWS instance

    python3 -m aws-instance START

STOP - Stop the AWS instance

    python3 -m aws-instance STOP

STATUS - Return the current state of the AWS instance

    python3 -m aws-instance STATUS
