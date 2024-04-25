#!/usr/bin/env bash


set -e
set -u
set -x





sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
/usr/local/bin/task --version
