#!/usr/bin/env bash


set -e
set -u
set -x





sudo apt-get -y install qemu-system-x86
sudo --user linuxbrew --login brew install podman
