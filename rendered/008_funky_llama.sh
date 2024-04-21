#!/usr/bin/env bash

set -e
set -u
set -x

if [[ -d /opt/ringgem ]]; then
    ! command -v git &>/dev/null && exit 0
    cd /opt/ringgem/
    git pull
fi

git --work-tree=/opt/ringgem --git-dir=/opt/ringgem/.git pull origin master
git --work-tree=/opt/ringgem --git-dir=/opt/ringgem/.git branch --set-upstream-to=origin/master master
git --git-dir=/opt/ringgem/.git pull
