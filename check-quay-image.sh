#!/bin/bash

# Script to check if a Quay image tag exists, fallback to default tag if not found
# Usage: ./check-quay-image.sh <quay-repo> <tag> <fallback-tag>

set -e

# Parse arguments
QUAY_REPO="${1}"
TAG="${2}"
FALLBACK_TAG="${3:-latest}"

# Validate inputs
if [ -z "$QUAY_REPO" ] || [ -z "$TAG" ]; then
    echo "Usage: $0 <quay-repo> <tag> [fallback-tag]"
    echo "Example: $0 quay.io/organization/repository v1.0.0 latest"
    exit 1
fi

# Function to check if image tag exists using skopeo
check_tag_skopeo() {
    local repo="$1"
    local tag="$2"

    if skopeo inspect "docker://${repo}:${tag}" &>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to get image details using skopeo
get_image_details() {
    local repo="$1"
    local tag="$2"

    echo "Fetching details for ${repo}:${tag}"
    skopeo inspect "docker://${repo}:${tag}"
}

# Main logic
echo "Checking for ${QUAY_REPO}:${TAG}..."

if check_tag_skopeo "$QUAY_REPO" "$TAG"; then
    echo "✓ Tag '${TAG}' found"
    get_image_details "$QUAY_REPO" "$TAG"
else
    echo "✗ Tag '${TAG}' not found"
    echo "Falling back to tag '${FALLBACK_TAG}'..."

    if check_tag_skopeo "$QUAY_REPO" "$FALLBACK_TAG"; then
        echo "✓ Fallback tag '${FALLBACK_TAG}' found"
        get_image_details "$QUAY_REPO" "$FALLBACK_TAG"
    else
        echo "✗ Fallback tag '${FALLBACK_TAG}' not found"
        exit 1
    fi
fi