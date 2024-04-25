#!/usr/bin/env bash


set -e
set -u
#set -x



if ! command -v git &>/dev/null; then
    echo git is not installed, exiting
    exit 0
fi

mkdir -p /opt/ringgem
cd /opt/ringgem

git init
git config user.email "you@example.com"
git config user.name "Your Name"

if ! git remote get-url origin &>/dev/null; then
    git remote add origin https://github.com/taylormonacelli/ringgem.git
fi

git fetch --depth 1

if ! git rev-parse --verify master &>/dev/null; then
    git checkout -b master origin/master
fi

git branch --set-upstream-to=origin/master master
git log --pretty=format:'%h%d %ar %s' --reverse -20
