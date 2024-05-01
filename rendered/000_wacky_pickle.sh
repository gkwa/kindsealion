#!/usr/bin/env bash


set -e
set -u
set -x





apt_update_with_retry() {
    max_retries=5
    retry_delay=10

    for ((i = 1; i <= max_retries; i++)); do
        sudo apt-get update && break
        if [ $i -eq $max_retries ]; then
            echo "Failed to run apt update after $max_retries attempts. Exiting."
            exit 1
        fi
        echo "apt update failed. Retrying in $retry_delay seconds... (Attempt $i/$max_retries)"
        sleep $retry_delay
    done
}

apt_update_with_retry
