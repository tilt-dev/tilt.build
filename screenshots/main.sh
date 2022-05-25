#!/bin/bash

# Make sure our kind wrapper gets called
PATH=.:$PATH
export TILT_DISABLE_ANALYTICS=1

cluster_created() {
    local context=$(kubectl config view -o jsonpath='{.current-context}')
    [ "$context" ]
}

cluster_create() {
    ctlptl apply -f cluster.yaml
}

cluster_up() {
    cluster_created && kubectl get nodes > /dev/null
}

cleanup() {
    cluster_created && ctlptl delete -f cluster.yaml
}

main() {
    set -ex
    trap cleanup EXIT

    mkdir -p /app/screenshots
    cluster_up || cluster_create

    python3 main.py
}

if [ "${0%bash}" = "$0" ]; then
    main
fi
