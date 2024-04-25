#!/usr/bin/env bash


set -e
set -u
set -x



echo running script:ringgem.sh


start_time=$(date +%s)
timeout=180

while true; do
    if ping -c 1 google.com &> /dev/null; then
        echo "Ping successful. Exiting with status 0."
        exit 0
    fi

    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    if [ $elapsed_time -ge $timeout ]; then
        echo "Ping failed for 3 minutes. Exiting with status 1."
        exit 1
    fi

    sleep 1
done



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
