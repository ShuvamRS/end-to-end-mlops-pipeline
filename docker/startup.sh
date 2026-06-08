#!/bin/bash

set -e

REPOSITORY_OWNER=ShuvamRS
REPOSITORY_NAME=end-to-end-mlops-pipeline

set_token() {
    REG_TOKEN=$(curl -s -X POST \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Authorization: token ${GITHUB_RUNNER_PAT}" \
        https://api.github.com/repos/${REPOSITORY_OWNER}/${REPOSITORY_NAME}/actions/runners/registration-token | jq -r .token)
}

set_token

./config.sh --unattended \
    --url https://github.com/${REPOSITORY_OWNER}/${REPOSITORY_NAME} \
    --replace \
    --labels ${GITHUB_RUNNER_LABEL} \
    --token ${REG_TOKEN}

cleanup() {
    echo "Removing runner..."
    set_token
    ./config.sh remove --unattended --token ${REG_TOKEN}
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

./run.sh > run.log 2>&1 & wait $!
