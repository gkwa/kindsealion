#!/usr/bin/env bash


set -e
set -u
set -x





task --dir=/opt/ringgem install-txtar-on-linux
sudo --login --user linuxbrew brew install golang
task --dir=/opt/ringgem install-nix-on-linux
task --dir=/opt/ringgem install-devbox-on-linux
task --dir=/opt/ringgem install-elasticsearch-on-ubuntu
task --dir=/opt/ringgem install-kibana-on-ubuntu
