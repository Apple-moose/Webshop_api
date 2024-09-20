#!/usr/bin/env bash

set -e

# Run migrations
pipenv run migrate

# Start the server
pipenv run start