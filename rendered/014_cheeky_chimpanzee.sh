#!/usr/bin/env bash

set -e
set -u
set -x


if [[ -d /opt/ringgem ]]; then
    ! command -v git &>/dev/null && exit 0
    cd /opt/ringgem/
    git pull
fi

task --dir=/opt/ringgem install-tofu-on-ubuntu
