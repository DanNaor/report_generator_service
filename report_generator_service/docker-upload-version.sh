#!/bin/bash

# Get the current version from pyproject.toml
CURRENT_VERSION=$(python3 -m poetry version | awk '{print $NF}')
PROJECT_NAME=$(poetry version | awk '{print $1}')

# Get the version number from pyproject.toml
VERSION=$(grep "^version = " pyproject.toml | cut -d '"' -f2)

# Parse the version components (major, minor, patch)
MAJOR=$(echo $VERSION | cut -d. -f1)
MINOR=$(echo $VERSION | cut -d. -f2)
PATCH=$(echo $VERSION | cut -d. -f3)

# Prompt the user for the version type (major, minor, or patch)
read -p "Enter the version type (major, minor, or patch): " VERSION_TYPE

# Increment the appropriate version component
if [[ "$VERSION_TYPE" == "major" ]]; then
    MAJOR=$((MAJOR+1))
    MINOR=0
    PATCH=0
elif [[ "$VERSION_TYPE" == "minor" ]]; then
    MINOR=$((MINOR+1))
    PATCH=0
elif [[ "$VERSION_TYPE" == "patch" ]]; then
    PATCH=$((PATCH+1))
else
    echo "Invalid version type"
    exit 1
fi


# Assemble the new version number
NEW_VERSION="$MAJOR.$MINOR.$PATCH"

# Update the version number in pyproject.toml
poetry version "$NEW_VERSION"

# Build the Docker image
docker build -t dannaor/rg:$NEW_VERSION .

# Push the Docker image to Docker Hub
docker push dannaor/rg:$NEW_VERSION

# Revert the version number in pyproject.toml
poetry version "$CURRENT_VERSION"