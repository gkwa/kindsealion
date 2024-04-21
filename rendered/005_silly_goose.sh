#!/usr/bin/env bash

set -e
set -u
set -x

if [[ -d /opt/ringgem ]]; then
    ! command -v git &>/dev/null && exit 0
    cd /opt/ringgem/
    git pull
fi

sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
/usr/local/bin/task --version
