#!/usr/bin/env bash


set -e
set -u
set -x





d=$(mktemp -d /tmp/golang-XXX)
cat >$d/Brewfile <<EOF
brew "golang"
brew "ansible"
EOF
chmod -R a+rwx $d
sudo --login --user linuxbrew bash -c "cd $d && brew bundle"
