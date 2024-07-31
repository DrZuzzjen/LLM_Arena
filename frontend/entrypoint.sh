#!/bin/bash

# Make sure the script fails on errors
set -e

# Run any setup commands here if needed

# Execute the CMD from the Dockerfile
exec "$@"