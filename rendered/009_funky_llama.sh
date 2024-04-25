#!/usr/bin/env bash

set -e
set -u
set -x

if [[ -d /opt/ringgem ]]; then
    ! command -v git &>/dev/null && exit 0
    cd /opt/ringgem/
    git pull
fi

cd /opt/ringgem
git config user.name "Your Name"
git config user.email "you@example.com"
git branch --set-upstream-to=origin/master master
git fetch
git reset --hard @{upstream}
