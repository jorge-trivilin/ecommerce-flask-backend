#!/bin/bash

# Gets the current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

git pull origin "$current_branch"

git commit --allow-empty -m "Trigger GitHub Actions workflow -build"

# Pushes to the current branch
git push origin "$current_branch"
