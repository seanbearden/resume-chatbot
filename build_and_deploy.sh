#!/bin/bash
# Set DOCKER_HOST and run sam build
DOCKER_HOST=unix:///Users/seanbearden/.docker/run/docker.sock sam build --use-container -t template.yaml
# Validate the SAM template
sam validate --lint
# Check if the first argument is "guided"
if [ "$1" == "guided" ]
then
    # Set DOCKER_HOST and run sam deploy with --guided
    DOCKER_HOST=unix:///Users/seanbearden/.docker/run/docker.sock sam deploy --guided
else
    # Set DOCKER_HOST and run sam deploy without --guided
    DOCKER_HOST=unix:///Users/seanbearden/.docker/run/docker.sock sam deploy
fi
