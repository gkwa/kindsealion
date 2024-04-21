#!/usr/bin/env bash

set -e
set -u
set -x

timeout=30
timeout_cmd="timeout ${timeout}s"

${timeout_cmd} bash -c '
 end_time=$(($(date +%s) + timeout))

 until ping -c 1 google.com &> /dev/null
 do
   current_time=$(date +%s)
   remaining_time=$((end_time - current_time))
   [[ $remaining_time -lt 0 ]] && break
   echo "Pinging Google... (${remaining_time}s remaining)"
   sleep 1
 done

 [[ $remaining_time -ge 0 ]] && echo "ping: google is reachable!"
' || echo "Timeout reached after ${timeout}s. Google is not reachable."
