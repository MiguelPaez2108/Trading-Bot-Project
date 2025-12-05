#!/bin/bash

# ============================================================================
# Trading System - Stop Script
# ============================================================================
# This script gracefully stops all services

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Trading System - Stopping Services${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Graceful shutdown with timeout
echo "Stopping services gracefully (30s timeout)..."
docker-compose stop -t 30

echo ""
echo "Removing containers..."
docker-compose down

echo ""
echo -e "${GREEN}✓${NC} All services stopped"
echo ""
