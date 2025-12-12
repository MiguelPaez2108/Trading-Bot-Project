#!/bin/bash
# Docker Management Scripts

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ==============================================================================
# Start all services
# ==============================================================================
start() {
    echo_info "Starting all services..."
    docker-compose up -d
    echo_info "Services started. Checking health..."
    sleep 5
    docker-compose ps
}

# ==============================================================================
# Start with management tools (pgAdmin, Redis Commander)
# ==============================================================================
start_with_tools() {
    echo_info "Starting all services with management tools..."
    docker-compose --profile tools up -d
    echo_info "Services started. Checking health..."
    sleep 5
    docker-compose ps
}

# ==============================================================================
# Stop all services
# ==============================================================================
stop() {
    echo_info "Stopping all services..."
    docker-compose down
    echo_info "Services stopped."
}

# ==============================================================================
# Restart all services
# ==============================================================================
restart() {
    echo_info "Restarting all services..."
    docker-compose restart
    echo_info "Services restarted."
}

# ==============================================================================
# View logs
# ==============================================================================
logs() {
    service=${1:-}
    if [ -z "$service" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$service"
    fi
}

# ==============================================================================
# Check service health
# ==============================================================================
health() {
    echo_info "Checking service health..."
    docker-compose ps
    echo ""
    echo_info "TimescaleDB:"
    docker-compose exec timescaledb pg_isready -U trader || echo_error "TimescaleDB not ready"
    echo ""
    echo_info "Redis:"
    docker-compose exec redis redis-cli ping || echo_error "Redis not ready"
}

# ==============================================================================
# Database shell
# ==============================================================================
db_shell() {
    echo_info "Connecting to TimescaleDB..."
    docker-compose exec timescaledb psql -U trader -d trading
}

# ==============================================================================
# Redis shell
# ==============================================================================
redis_shell() {
    echo_info "Connecting to Redis..."
    docker-compose exec redis redis-cli
}

# ==============================================================================
# Run migrations
# ==============================================================================
migrate() {
    echo_info "Running database migrations..."
    docker-compose exec trading-system alembic upgrade head
    echo_info "Migrations complete."
}

# ==============================================================================
# Clean everything (WARNING: Deletes all data)
# ==============================================================================
clean() {
    echo_warn "This will delete ALL data including databases. Are you sure? (yes/no)"
    read -r response
    if [ "$response" = "yes" ]; then
        echo_info "Stopping services..."
        docker-compose down -v
        echo_info "Removing volumes..."
        docker volume rm trading-bot-project_timescale_data || true
        docker volume rm trading-bot-project_redis_data || true
        docker volume rm trading-bot-project_prometheus_data || true
        docker volume rm trading-bot-project_grafana_data || true
        echo_info "Clean complete."
    else
        echo_info "Clean cancelled."
    fi
}

# ==============================================================================
# Build images
# ==============================================================================
build() {
    echo_info "Building Docker images..."
    docker-compose build --no-cache
    echo_info "Build complete."
}

# ==============================================================================
# Show help
# ==============================================================================
help() {
    echo "Docker Management Script"
    echo ""
    echo "Usage: ./scripts/docker.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start           - Start all services"
    echo "  start-tools     - Start all services with management tools"
    echo "  stop            - Stop all services"
    echo "  restart         - Restart all services"
    echo "  logs [service]  - View logs (optionally for specific service)"
    echo "  health          - Check service health"
    echo "  db-shell        - Open PostgreSQL shell"
    echo "  redis-shell     - Open Redis shell"
    echo "  migrate         - Run database migrations"
    echo "  build           - Build Docker images"
    echo "  clean           - Remove all containers and volumes (WARNING: deletes data)"
    echo "  help            - Show this help message"
}

# ==============================================================================
# Main
# ==============================================================================
case "${1:-}" in
    start)
        start
        ;;
    start-tools)
        start_with_tools
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs "${2:-}"
        ;;
    health)
        health
        ;;
    db-shell)
        db_shell
        ;;
    redis-shell)
        redis_shell
        ;;
    migrate)
        migrate
        ;;
    build)
        build
        ;;
    clean)
        clean
        ;;
    help|*)
        help
        ;;
esac
