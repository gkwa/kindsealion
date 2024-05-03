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
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
export DEBIAN_FRONTEND=noninteractive
sudo dpkg-reconfigure locales
sudo --login --user linuxbrew brew install taylormonacelli/homebrew-tools/itmetrics
