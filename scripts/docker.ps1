<#
.SYNOPSIS
    Docker Management Script for Trading Bot
    
.DESCRIPTION
    Manages the lifecycle of the Trading Bot Docker containers.
    
.PARAMETER Command
    The command to execute (start, stop, restart, logs, health, etc.)
    
.EXAMPLE
    .\scripts\docker.ps1 start
#>

param (
    [Parameter(Mandatory=$false, Position=0)]
    [ValidateSet("start", "start-tools", "stop", "restart", "logs", "health", "db-shell", "redis-shell", "migrate", "build", "clean", "help")]
    [string]$Command = "help",

    [Parameter(Mandatory=$false, Position=1)]
    [string]$Service
)

$ErrorActionPreference = "Stop"

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Show-Help {
    Write-Host "Docker Management Script (PowerShell)"
    Write-Host ""
    Write-Host "Usage: .\scripts\docker.ps1 [command]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  start           - Start all services"
    Write-Host "  start-tools     - Start all services with management tools"
    Write-Host "  stop            - Stop all services"
    Write-Host "  restart         - Restart all services"
    Write-Host "  logs [service]  - View logs (optionally for specific service)"
    Write-Host "  health          - Check service health"
    Write-Host "  db-shell        - Open PostgreSQL shell"
    Write-Host "  redis-shell     - Open Redis shell"
    Write-Host "  migrate         - Run database migrations"
    Write-Host "  build           - Build Docker images"
    Write-Host "  clean           - Remove all containers and volumes (WARNING: deletes data)"
    Write-Host "  help            - Show this help message"
}

switch ($Command) {
    "start" {
        Write-Info "Starting all services..."
        docker-compose up -d
        Write-Info "Services started. Checking health..."
        Start-Sleep -Seconds 5
        docker-compose ps
    }

    "start-tools" {
        Write-Info "Starting all services with management tools..."
        docker-compose --profile tools up -d
        Write-Info "Services started. Checking health..."
        Start-Sleep -Seconds 5
        docker-compose ps
    }

    "stop" {
        Write-Info "Stopping all services..."
        docker-compose down
        Write-Info "Services stopped."
    }

    "restart" {
        Write-Info "Restarting all services..."
        docker-compose restart
        Write-Info "Services restarted."
    }

    "logs" {
        if ([string]::IsNullOrEmpty($Service)) {
            docker-compose logs -f
        } else {
            docker-compose logs -f $Service
        }
    }

    "health" {
        Write-Info "Checking service health..."
        docker-compose ps
        Write-Host ""
        Write-Info "TimescaleDB:"
        try {
            docker-compose exec timescaledb pg_isready -U trader -d trading
        } catch {
            Write-ErrorMsg "TimescaleDB not ready"
        }
        Write-Host ""
        Write-Info "Redis:"
        try {
            docker-compose exec redis redis-cli ping
        } catch {
            Write-ErrorMsg "Redis not ready"
        }
    }

    "db-shell" {
        Write-Info "Connecting to TimescaleDB..."
        docker-compose exec timescaledb psql -U trader -d trading
    }

    "redis-shell" {
        Write-Info "Connecting to Redis..."
        docker-compose exec redis redis-cli
    }

    "migrate" {
        Write-Info "Running database migrations..."
        docker-compose exec trading-system alembic upgrade head
        Write-Info "Migrations complete."
    }

    "build" {
        Write-Info "Building Docker images..."
        docker-compose build --no-cache
        Write-Info "Build complete."
    }

    "clean" {
        Write-Warn "This will delete ALL data including databases. Are you sure? (yes/no)"
        $response = Read-Host
        if ($response -eq "yes") {
            Write-Info "Stopping services..."
            docker-compose down -v
            Write-Info "Removing volumes..."
            docker volume rm trading-bot-project_timescale_data -ErrorAction SilentlyContinue
            docker volume rm trading-bot-project_redis_data -ErrorAction SilentlyContinue
            docker volume rm trading-bot-project_prometheus_data -ErrorAction SilentlyContinue
            docker volume rm trading-bot-project_grafana_data -ErrorAction SilentlyContinue
            Write-Info "Clean complete."
        } else {
            Write-Info "Clean cancelled."
        }
    }

    "help" {
        Show-Help
    }

    Default {
        Show-Help
    }
}
