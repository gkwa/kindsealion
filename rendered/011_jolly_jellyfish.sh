#!/usr/bin/env bash


set -e
set -u
set -x





task --dir=/opt/ringgem install-elasticsearch-on-ubuntu
task --dir=/opt/ringgem install-kibana-on-ubuntu
