wait_for_dns() {
    start_time=$(date +%s)
    timeout=180

    while true; do
        if ping -c 1 google.com &> /dev/null; then
            echo "Ping successful. Exiting with status 0."
            return 0
        fi

        current_time=$(date +%s)
        elapsed_time=$((current_time - start_time))

        if [ $elapsed_time -ge $timeout ]; then
            echo "Ping failed for 3 minutes. Exiting with status 1."
            return 1
        fi

        sleep 1
    done
}

wait_for_dns
