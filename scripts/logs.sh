#!/bin/bash

# ============================================================================
# Trading System - Logs Script
# ============================================================================
# View aggregated logs from all services

# Default: follow logs
FOLLOW="-f"

# Parse arguments
if [ "$1" == "--no-follow" ]; then
    FOLLOW=""
fi

# Show logs
docker-compose logs $FOLLOW --tail=100
