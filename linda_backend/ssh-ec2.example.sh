#!/bin/bash

# AWS ECS setup

KEY_FILE="PATH_TO_KEYFILE"

if [ ! -f "$KEY_FILE" ]; then
    echo "Key file does not exist"
    exit 1
fi

PERMISSIONS=$(stat -c "%a" "$KEY_FILE")
EC2_USER="EC2_USER"
EC2_HOST="HOST_URL"

if [ "$PERMISSIONS" -eq 400 ]; then
    echo "File Permission already satisfied"
else
    echo "Setting File permission"
    chmod 400 "$KEY_FILE"
    echo "Permissions set to 400"
fi

echo "Connection to AWS EC2"
ssh -i "$KEY_FILE" "$EC2_USER"@"$EC2_HOST"

