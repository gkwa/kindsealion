#!/usr/bin/env bash


set -e
set -u
set -x





sudo --login --user linuxbrew brew install taylormonacelli/homebrew-tools/itmetrics
sudo --login --user linuxbrew brew install golang
task --dir=/opt/ringgem install-txtar-on-linux
