#!/usr/bin/env bash

set -e
set -u
set -x

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
        echo "Ping failed after $timeout seconds.  Exiting with status 1."
        exit 1
    fi

    sleep 2s
done
