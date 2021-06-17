#!/bin/bash

# Source environment variables
export $(xargs < .env)
export FLASK_ENV=production

# Run python script
python "$@"
