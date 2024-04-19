#!/usr/bin/env bash

set -e
set -u

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

echo pulling latest from $(git remote v | head -1 | awk '{print $2}')
cd /opt/ringgem
git pull
