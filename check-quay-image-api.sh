#!/bin/bash

# Script to check if a Quay image tag exists using Quay API
# Usage: ./check-quay-image-api.sh <namespace/repository> <tag> <fallback-tag>

set -e

# Parse arguments
REPO_PATH="${1}"  # e.g., "organization/repository"
TAG="${2}"
FALLBACK_TAG="${3:-latest}"

# Validate inputs
if [ -z "$REPO_PATH" ] || [ -z "$TAG" ]; then
    echo "Usage: $0 <namespace/repository> <tag> [fallback-tag]"
    echo "Example: $0 opendatahub/notebook-images v1.0.0 latest"
    exit 1
fi

QUAY_API="https://quay.io/api/v1"

# Function to check if tag exists using Quay API
check_tag_api() {
    local repo_path="$1"
    local tag="$2"

    response=$(curl -s "${QUAY_API}/repository/${repo_path}/tag/?specificTag=${tag}")
    tag_count=$(echo "$response" | jq -r '.tags | length')

    if [ "$tag_count" -gt 0 ]; then
        return 0
    else
        return 1
    fi
}

# Function to get image details using Quay API
get_image_details() {
    local repo_path="$1"
    local tag="$2"

    echo "Fetching details for ${repo_path}:${tag}"
    response=$(curl -s "${QUAY_API}/repository/${repo_path}/tag/?specificTag=${tag}")

    echo "$response" | jq '{
        name: .tags[0].name,
        manifest_digest: .tags[0].manifest_digest,
        size: .tags[0].size,
        last_modified: .tags[0].last_modified,
        image_id: .tags[0].image_id
    }'
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed"
    exit 1
fi

# Main logic
echo "Checking for ${REPO_PATH}:${TAG}..."

if check_tag_api "$REPO_PATH" "$TAG"; then
    echo "✓ Tag '${TAG}' found"
    get_image_details "$REPO_PATH" "$TAG"
else
    echo "✗ Tag '${TAG}' not found"
    echo "Falling back to tag '${FALLBACK_TAG}'..."

    if check_tag_api "$REPO_PATH" "$FALLBACK_TAG"; then
        echo "✓ Fallback tag '${FALLBACK_TAG}' found"
        get_image_details "$REPO_PATH" "$FALLBACK_TAG"
    else
        echo "✗ Fallback tag '${FALLBACK_TAG}' not found"
        exit 1
    fi
fi