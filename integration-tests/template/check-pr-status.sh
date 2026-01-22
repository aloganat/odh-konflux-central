#!/bin/bash

set -e

# Configuration - set these variables or pass as environment variables
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
REPO_OWNER="${REPO_OWNER:-}"
REPO_NAME="${REPO_NAME:-}"
PR_NUMBER="${PR_NUMBER:-}"

# Usage message
usage() {
    echo "Usage: $0"
    echo "Required environment variables:"
    echo "  GITHUB_TOKEN - GitHub personal access token"
    echo "  REPO_OWNER   - Repository owner/organization"
    echo "  REPO_NAME    - Repository name"
    echo "  PR_NUMBER    - Pull request number"
    exit 1
}

# Validate required parameters
if [ -z "$GITHUB_TOKEN" ] || [ -z "$REPO_OWNER" ] || [ -z "$REPO_NAME" ] || [ -z "$PR_NUMBER" ]; then
    echo "Error: Missing required environment variables"
    usage
fi

# GitHub API endpoints
API_BASE="https://api.github.com"
PR_URL="$API_BASE/repos/$REPO_OWNER/$REPO_NAME/pulls/$PR_NUMBER"
COMMENTS_URL="$API_BASE/repos/$REPO_OWNER/$REPO_NAME/issues/$PR_NUMBER/comments"

echo "Fetching PR information..."
# Get the PR to find the head SHA
PR_DATA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$PR_URL")

HEAD_SHA=$(echo "$PR_DATA" | jq -r '.head.sha')

if [ -z "$HEAD_SHA" ] || [ "$HEAD_SHA" = "null" ]; then
    echo "Error: Could not retrieve HEAD SHA for PR #$PR_NUMBER"
    exit 1
fi

echo "HEAD SHA: $HEAD_SHA"

# Get check runs for the commit
echo "Fetching check runs..."
CHECK_RUNS_URL="$API_BASE/repos/$REPO_OWNER/$REPO_NAME/commits/$HEAD_SHA/check-runs"
CHECK_RUNS_DATA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "$CHECK_RUNS_URL")

# Extract check runs with names starting with "Red Hat Konflux"
echo "Analyzing check runs..."
KONFLUX_CHECKS=$(echo "$CHECK_RUNS_DATA" | jq -r '.check_runs[] | select(.name | startswith("Red Hat Konflux")) | "\(.name)|\(.status)"')

if [ -z "$KONFLUX_CHECKS" ]; then
    echo "No Red Hat Konflux checks found"
    exit 0
fi

echo "Found Red Hat Konflux checks:"
echo "$KONFLUX_CHECKS"

# Check if all Konflux checks are completed (except odh-group-test)
ALL_COMPLETED=true
while IFS='|' read -r name status; do
    # Skip the check with "odh-group-test" in its name
    if [[ "$name" == *"odh-group-test"* ]]; then
        echo "Skipping check: $name (contains odh-group-test)"
        continue
    fi

    if [ "$status" != "completed" ]; then
        echo "Check not completed: $name (status: $status)"
        ALL_COMPLETED=false
    else
        echo "Check completed: $name"
    fi
done <<< "$KONFLUX_CHECKS"

# If all checks are completed, add comment
if [ "$ALL_COMPLETED" = true ]; then
    echo "All Red Hat Konflux checks (except odh-group-test) are completed!"
    echo "Adding /group-test comment to PR #$PR_NUMBER..."

    curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        -d '{"body":"/group-test"}' \
        "$COMMENTS_URL" > /dev/null

    echo "Comment added successfully!"
else
    echo "Not all checks are completed yet. Skipping comment."
fi
