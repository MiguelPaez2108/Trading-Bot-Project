#!/bin/bash

# ============================================================================
# Trading System - Start Script
# ============================================================================
# This script starts all services required for the trading system

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Trading System - Starting Services${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker is running"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env file with your configuration${NC}"
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo -e "${GREEN}✓${NC} Environment variables loaded"

# Start Docker Compose services
echo ""
echo "Starting Docker Compose services..."
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to be healthy..."
sleep 5

# Check TimescaleDB
echo -n "Checking TimescaleDB... "
if docker-compose exec -T timescaledb pg_isready -U ${POSTGRES_USER:-trading_user} > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo -e "${RED}TimescaleDB is not ready${NC}"
    exit 1
fi

# Check Redis Cache
echo -n "Checking Redis Cache... "
if docker-compose exec -T redis-cache redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo -e "${RED}Redis Cache is not ready${NC}"
    exit 1
fi

# Check Redis Streams
echo -n "Checking Redis Streams... "
if docker-compose exec -T redis-streams redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo -e "${RED}Redis Streams is not ready${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  All services are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Service URLs:"
echo "  - TimescaleDB:  localhost:${POSTGRES_PORT:-5432}"
echo "  - Redis Cache:  localhost:${REDIS_CACHE_PORT:-6379}"
echo "  - Redis Streams: localhost:${REDIS_STREAMS_PORT:-6380}"
echo "  - Prometheus:   http://localhost:${PROMETHEUS_PORT:-9090}"
echo "  - Grafana:      http://localhost:${GRAFANA_PORT:-3000}"
echo ""
echo "Grafana credentials:"
echo "  - Username: ${GRAFANA_ADMIN_USER:-admin}"
echo "  - Password: ${GRAFANA_ADMIN_PASSWORD:-admin}"
echo ""
echo "To view logs: ./scripts/logs.sh"
echo "To stop:      ./scripts/stop.sh"
echo ""
