# Script para crear la estructura completa de carpetas del sistema de trading

$baseDir = "c:\Users\Asus\OneDrive\Escritorio\Trading-Bot Project"

# Lista de todos los directorios a crear
$directories = @(
    # src/python - Domain Layer
    "src\python\domain\entities",
    "src\python\domain\value_objects",
    "src\python\domain\repositories",
    "src\python\domain\services",
    "src\python\domain\events",
    
    # src/python - Application Layer
    "src\python\application\use_cases",
    "src\python\application\dto",
    "src\python\application\ports",
    
    # src/python - Strategies
    "src\python\strategies\base",
    "src\python\strategies\momentum",
    "src\python\strategies\mean_reversion",
    "src\python\strategies\market_making",
    "src\python\strategies\arbitrage",
    "src\python\strategies\grid",
    "src\python\strategies\ml",
    
    # src/python - Market Data
    "src\python\market_data\feeds",
    "src\python\market_data\processors",
    "src\python\market_data\storage",
    "src\python\market_data\replay",
    
    # src/python - Scanners
    "src\python\scanners\base",
    "src\python\scanners\implementations",
    
    # src/python - Regime Detection
    "src\python\regime_detection\features",
    
    # src/python - Execution
    "src\python\execution\engine",
    "src\python\execution\order_types",
    "src\python\execution\retry",
    "src\python\execution\simulation",
    
    # src/python - Risk Management
    "src\python\risk_management\pre_trade",
    "src\python\risk_management\in_trade",
    "src\python\risk_management\portfolio",
    "src\python\risk_management\circuit_breakers",
    
    # src/python - Backtesting
    "src\python\backtesting\engine",
    "src\python\backtesting\data",
    "src\python\backtesting\simulation",
    "src\python\backtesting\optimization",
    "src\python\backtesting\metrics",
    "src\python\backtesting\validation",
    
    # src/python - Portfolio
    "src\python\portfolio",
    
    # src/python - Alerting
    "src\python\alerting\channels",
    
    # src/python - Infrastructure
    "src\python\infrastructure\exchanges",
    "src\python\infrastructure\database\migrations",
    "src\python\infrastructure\message_bus",
    "src\python\infrastructure\config\environments",
    "src\python\infrastructure\logging",
    
    # src/python - Monitoring
    "src\python\monitoring\dashboards",
    
    # src/python - API
    "src\python\api\rest\routers",
    "src\python\api\rest\middleware",
    "src\python\api\rest\schemas",
    "src\python\api\websocket",
    
    # src/python - CLI
    "src\python\cli\commands",
    
    # src/cpp - C++ Components
    "src\cpp\execution",
    "src\cpp\market_data",
    "src\cpp\indicators",
    "src\cpp\bindings",
    
    # tests
    "tests\unit\domain",
    "tests\unit\strategies",
    "tests\unit\risk_management",
    "tests\unit\scanners",
    "tests\unit\execution",
    "tests\integration",
    "tests\performance",
    "tests\chaos",
    
    # config
    "config\strategies",
    
    # data
    "data\historical",
    "data\backtests",
    "data\scans",
    "data\logs",
    
    # scripts
    "scripts",
    
    # docker
    "docker",
    
    # docs
    "docs\architecture\diagrams",
    "docs\api",
    "docs\strategies",
    "docs\deployment",
    
    # monitoring
    "monitoring\grafana",
    "monitoring\alerts",
    
    # notebooks
    "notebooks\research",
    "notebooks\backtesting"
)

# Crear todos los directorios
foreach ($dir in $directories) {
    $fullPath = Join-Path $baseDir $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "✓ Creado: $dir" -ForegroundColor Green
    } else {
        Write-Host "○ Ya existe: $dir" -ForegroundColor Yellow
    }
}

Write-Host "`n✅ Estructura de carpetas creada exitosamente!" -ForegroundColor Cyan
