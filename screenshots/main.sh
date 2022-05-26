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

tilt_up_and_wait() {
    tilt up --legacy=false --stream=true -f $@ &
    local i=0
    while ! curl -sf localhost:10350 > /dev/null; do
        if [ $i -gt 10 ]; then
            echo "Timed out waiting for Tilt"
            exit 1
        fi
        sleep 1
        i=$[ $i + 1 ]
    done
    tilt wait --all --for=condition=Ready uiresource
}

tilt_pid() {
    tilt get session -o jsonpath='{.items[0].status.pid}'
}

main() {
    set -ex
    trap cleanup EXIT

    mkdir -p /app/screenshots
    cluster_up || cluster_create

    [ -d tilt-example-html ] || \
        git clone https://github.com/tilt-dev/tilt-example-html

    tilt_up_and_wait tilt-example-html/0-*/Tiltfile

    python3 screenshot.py
    kill $(tilt_pid)
}

if [ "${0%bash}" = "$0" ]; then
    main
fi
