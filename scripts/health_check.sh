#!/bin/bash

# ============================================================================
# Trading System - Health Check Script
# ============================================================================
# Returns exit code 0 if all services are healthy, 1 otherwise

set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

EXIT_CODE=0

# Check TimescaleDB
if docker-compose exec -T timescaledb pg_isready -U ${POSTGRES_USER:-trading_user} > /dev/null 2>&1; then
    echo "✓ TimescaleDB: healthy"
else
    echo "✗ TimescaleDB: unhealthy"
    EXIT_CODE=1
fi

# Check Redis Cache
if docker-compose exec -T redis-cache redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis Cache: healthy"
else
    echo "✗ Redis Cache: unhealthy"
    EXIT_CODE=1
fi

# Check Redis Streams
if docker-compose exec -T redis-streams redis-cli ping > /dev/null 2>&1; then
    echo "✓ Redis Streams: healthy"
else
    echo "✗ Redis Streams: unhealthy"
    EXIT_CODE=1
fi

# Check Prometheus
if curl -s http://localhost:${PROMETHEUS_PORT:-9090}/-/healthy > /dev/null 2>&1; then
    echo "✓ Prometheus: healthy"
else
    echo "✗ Prometheus: unhealthy"
    EXIT_CODE=1
fi

# Check Grafana
if curl -s http://localhost:${GRAFANA_PORT:-3000}/api/health > /dev/null 2>&1; then
    echo "✓ Grafana: healthy"
else
    echo "✗ Grafana: unhealthy"
    EXIT_CODE=1
fi

exit $EXIT_CODE
