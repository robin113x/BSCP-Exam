#!/bin/bash

while true; do

    if [[ -n $(git status --porcelain) ]]; then
        echo "Changes detected in repository. Committing and pushing changes..."
        git pull
        git add -A
        git commit -m "Robin h00d"
        git push
        echo "Changes committed and pushed successfully."
    fi
    sleep 5
done 