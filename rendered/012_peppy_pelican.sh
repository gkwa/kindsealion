#!/usr/bin/env bash


set -e
set -u
set -x





set -e
set -x
set -u

d=$(mktemp -d /tmp/golang-XXX)
cat >$d/Brewfile <<EOF
brew "golang"
brew "ansible"
EOF
chmod -R a+rwx $d
sudo --login --user linuxbrew bash -c "cd $d && brew bundle"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales
sudo --login --user linuxbrew brew install taylormonacelli/homebrew-tools/itmetrics

rm -rf $d
