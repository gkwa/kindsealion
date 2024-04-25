#!/usr/bin/env bash

set -e
set -u
set -x

if [[ ! -d /opt/ringgem ]]; then
    echo "/opt/ringgem doesn't exist, exiting"
    exit 0
fi

if ! command -v git &>/dev/null; then
    echo git is not installed, exiting
    exit 0
fi

# wait for dns
timeout 20s curl --retry 9999 --connect-timeout 1 -sSf https://www.google.com >/dev/null

cd /opt/ringgem
echo pulling latest from $(git remote --verbose | head -1 | awk '{print $2}')
git pull
