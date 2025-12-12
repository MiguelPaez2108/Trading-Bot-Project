# 🎯 PROMPT MAESTRO V2.0: Sistema de Trading Algorítmico Institucional
## Enhanced with Production Insights from Moon Dev

Eres un arquitecto de software senior especializado en sistemas de trading de alta frecuencia con 15+ años de experiencia en fondos cuantitativos. Tu tarea es diseñar e implementar un sistema de trading algorítmico de nivel institucional **PRODUCTION-READY**.

---

## 🎭 CONTEXTO Y ROL

**Rol**: Actúa como un Lead Architect de un hedge fund cuantitativo que ha construido sistemas que manejan millones en volumen diario.

**Objetivo**: Crear un sistema de trading completo, robusto, escalable y production-ready que pueda:
- Operar 24/7 con uptime del 99.9%
- Ejecutar múltiples estrategias simultáneamente
- Manejar datos de mercado en tiempo real con latencia <100ms
- Soportar backtesting riguroso con datos históricos
- Escalar desde 1 a 100+ instrumentos
- Generar retornos consistentes con riesgo controlado

---

## ⚠️ FILOSOFÍA CRÍTICA: PROCESO RBI (Research → Backtest → Implement)

**REGLA DE ORO**: NUNCA saltar directo a construir bots sin validación previa.

```
┌─────────────────────────────────────────────────┐
│  RESEARCH (70% del tiempo total)                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  - Google Scholar (papers académicos)           │
│  - Libros de trading especializados            │
│  - Análisis de regímenes de mercado            │
│  - Generación y validación de ideas            │
│  - Estudio de traders exitosos (Jim Simons)    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  BACKTEST (25% del tiempo total)                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  - Test en MÚLTIPLES símbolos (min 5+)         │
│  - Test en MÚLTIPLES timeframes                 │
│  - Walk-forward optimization                    │
│  - Out-of-sample validation                     │
│  - Survivorship bias checks                     │
│  - Heat maps de optimización                    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  IMPLEMENT (5% del tiempo total)                │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  - Bot es la parte FÁCIL                        │
│  - Empezar con size TINY ($10-$50)             │
│  - Escalar gradualmente basado en resultados   │
│  - Monitorear y ajustar continuamente          │
└─────────────────────────────────────────────────┘
```

**ADVERTENCIA**: Si saltas directo a implementar = REKT garantizado.

---

## 📐 PARTE 1: ARQUITECTURA SCREAMING ARCHITECTURE

### 1.1 Principios de Clean Architecture

**Capas independientes**:
- Domain → Application → Infrastructure → Presentation
- Inversión de dependencias estricta
- Entities que representen conceptos de trading puros
- Use cases explícitos para cada operación

### 1.2 Estructura de Carpetas COMPLETA (3+ niveles)

```
trading-system/
│
├── 📁 src/
│   │
│   ├── 📁 python/                          # Core del sistema (Python)
│   │   │
│   │   ├── 📁 domain/                      # Capa de dominio pura (ZERO deps externas)
│   │   │   ├── 📁 entities/                # Entidades de negocio
│   │   │   │   ├── order.py               # Order, OrderType, OrderSide, OrderStatus
│   │   │   │   ├── trade.py               # Trade execution record
│   │   │   │   ├── position.py            # Open position tracking
│   │   │   │   ├── candle.py              # OHLCV candle
│   │   │   │   ├── orderbook.py           # Bid/Ask orderbook snapshot
│   │   │   │   ├── signal.py              # Trading signal entity
│   │   │   │   └── portfolio.py           # Portfolio state
│   │   │   ├── 📁 value_objects/          # Immutable value objects
│   │   │   │   ├── symbol.py              # TradingPair (BTC/USDT)
│   │   │   │   ├── money.py               # Decimal-based money
│   │   │   │   ├── timeframe.py           # 1m, 5m, 1h, 1d intervals
│   │   │   │   └── price.py               # Price with precision
│   │   │   ├── 📁 repositories/           # Repository interfaces (abstracciones)
│   │   │   │   ├── order_repository.py    # Interface para persistir órdenes
│   │   │   │   ├── trade_repository.py    # Interface para trades
│   │   │   │   ├── candle_repository.py   # Interface para market data
│   │   │   │   └── signal_repository.py   # Interface para signals
│   │   │   ├── 📁 services/               # Domain services
│   │   │   │   ├── risk_calculator.py     # Cálculos de riesgo puros
│   │   │   │   ├── pnl_calculator.py      # P&L calculations
│   │   │   │   ├── fee_calculator.py      # Maker/taker fees
│   │   │   │   └── slippage_calculator.py # Slippage estimation
│   │   │   └── 📁 events/                 # Domain events
│   │   │       ├── order_events.py        # OrderCreated, OrderFilled, etc.
│   │   │       ├── trade_events.py        # TradeExecuted, TradeRejected
│   │   │       └── market_events.py       # PriceUpdated, OrderBookChanged
│   │   │
│   │   ├── 📁 application/                # Use cases y orchestration
│   │   │   ├── 📁 use_cases/              # Application use cases
│   │   │   │   ├── execute_order.py       # UC: Ejecutar una orden
│   │   │   │   ├── cancel_order.py        # UC: Cancelar orden
│   │   │   │   ├── calculate_position.py  # UC: Calcular posición actual
│   │   │   │   ├── backtest_strategy.py   # UC: Correr backtest
│   │   │   │   ├── optimize_params.py     # UC: Optimizar parámetros
│   │   │   │   └── scan_market.py         # UC: Escanear mercado (NUEVO)
│   │   │   ├── 📁 dto/                    # Data Transfer Objects
│   │   │   │   ├── order_dto.py
│   │   │   │   ├── strategy_dto.py
│   │   │   │   ├── backtest_dto.py
│   │   │   │   └── scan_result_dto.py     # (NUEVO)
│   │   │   └── 📁 ports/                  # Interfaces para infra
│   │   │       ├── exchange_port.py       # Interface para exchanges
│   │   │       ├── market_data_port.py    # Interface para market data
│   │   │       ├── notification_port.py   # Interface para alertas
│   │   │       └── liquidation_port.py    # Interface liquidations (NUEVO)
│   │   │
│   │   ├── 📁 strategies/                 # Strategy implementations
│   │   │   ├── 📁 base/                   # Base classes y protocols
│   │   │   │   ├── strategy.py            # Abstract Strategy base class
│   │   │   │   ├── indicator.py           # Indicator protocol
│   │   │   │   └── signal.py              # Signal generation protocol
│   │   │   ├── 📁 momentum/               # Momentum-based strategies
│   │   │   │   ├── rsi_macd.py            # RSI + MACD momentum
│   │   │   │   ├── breakout.py            # Breakout strategy (MOON DEV)
│   │   │   │   └── trend_following.py     # Trend following
│   │   │   ├── 📁 mean_reversion/         # Mean reversion strategies
│   │   │   │   ├── bollinger_bands.py     # BB mean reversion
│   │   │   │   ├── zscore.py              # Z-score reversion
│   │   │   │   └── pairs_trading.py       # Pairs trading
│   │   │   ├── 📁 market_making/          # Market making strategies
│   │   │   │   ├── simple_mm.py           # Basic market maker
│   │   │   │   └── inventory_mm.py        # Inventory-aware MM
│   │   │   ├── 📁 arbitrage/              # Arbitrage strategies
│   │   │   │   ├── cross_exchange.py      # Cross-exchange arb
│   │   │   │   └── triangular.py          # Triangular arbitrage
│   │   │   ├── 📁 grid/                   # Grid trading
│   │   │   │   ├── standard_grid.py       # Standard grid
│   │   │   │   └── dynamic_grid.py        # Dynamic grid
│   │   │   └── 📁 ml/                     # ML-based strategies (optional)
│   │   │       ├── rl_strategy.py         # Reinforcement learning
│   │   │       └── lstm_predictor.py      # LSTM price prediction
│   │   │
│   │   ├── 📁 market_data/                # Market data engine
│   │   │   ├── 📁 feeds/                  # Exchange feeds
│   │   │   │   ├── base_feed.py           # Abstract feed interface
│   │   │   │   ├── binance_feed.py        # Binance WebSocket + REST
│   │   │   │   ├── hyperliquid_feed.py    # HyperLiquid feed (NUEVO)
│   │   │   │   ├── coinbase_feed.py       # Coinbase feed
│   │   │   │   ├── liquidations_feed.py   # Liquidations WebSocket (NUEVO)
│   │   │   │   └── aggregated_feed.py     # Multi-exchange aggregator
│   │   │   ├── 📁 processors/             # Data processors
│   │   │   │   ├── normalizer.py          # Normalize data entre exchanges
│   │   │   │   ├── validator.py           # Validate data integrity
│   │   │   │   ├── gap_detector.py        # Detect and handle gaps
│   │   │   │   └── aggregator.py          # Aggregate multi-source data
│   │   │   ├── 📁 storage/                # Data storage
│   │   │   │   ├── timeseries_writer.py   # Write to TimescaleDB
│   │   │   │   ├── cache_manager.py       # Redis cache
│   │   │   │   ├── csv_writer.py          # CSV export (NUEVO)
│   │   │   │   └── compressor.py          # Data compression
│   │   │   └── 📁 replay/                 # Historical replay
│   │   │       ├── replay_engine.py       # Replay historical data
│   │   │       └── speed_controller.py    # Control replay speed
│   │   │
│   │   ├── 📁 scanners/                   # Market scanning system (NUEVO)
│   │   │   ├── 📁 base/
│   │   │   │   ├── scanner.py             # Abstract scanner base class
│   │   │   │   └── scanner_result.py      # Scanner result object
│   │   │   ├── 📁 implementations/
│   │   │   │   ├── breakout_scanner.py    # Scan for breakouts
│   │   │   │   ├── volume_scanner.py      # Scan for volume spikes
│   │   │   │   ├── momentum_scanner.py    # Scan for momentum
│   │   │   │   ├── liquidity_scanner.py   # Scan liquidation zones (NUEVO)
│   │   │   │   └── regime_scanner.py      # Scan market regime (NUEVO)
│   │   │   ├── scanner_engine.py          # Main scanner orchestrator
│   │   │   └── scanner_config.py          # Scanner configuration
│   │   │
│   │   ├── 📁 regime_detection/           # Market regime detection (NUEVO)
│   │   │   ├── regime_classifier.py       # Classify current regime
│   │   │   ├── 📁 features/
│   │   │   │   ├── volatility_features.py # VIX, ATR, etc.
│   │   │   │   ├── trend_features.py      # SMA slopes, ADX
│   │   │   │   ├── volume_features.py     # Volume analysis
│   │   │   │   └── correlation_features.py# Asset correlations
│   │   │   ├── regime_types.py            # 8 regime definitions (Jim Simons)
│   │   │   └── strategy_mapper.py         # Map regime → optimal strategies
│   │   │
│   │   ├── 📁 execution/                  # Order execution (Python orchestration)
│   │   │   ├── 📁 engine/                 # Execution engine
│   │   │   │   ├── executor.py            # Main executor
│   │   │   │   ├── router.py              # Smart order routing
│   │   │   │   ├── validator.py           # Pre-execution validation
│   │   │   │   ├── position_tracker.py    # Real-time position tracking
│   │   │   │   └── order_manager.py       # Manage order lifecycle (NUEVO)
│   │   │   ├── 📁 order_types/            # Order type handlers
│   │   │   │   ├── market.py              # Market orders
│   │   │   │   ├── limit.py               # Limit orders
│   │   │   │   ├── stop_loss.py           # Stop loss orders
│   │   │   │   ├── take_profit.py         # Take profit
│   │   │   │   └── oco.py                 # OCO (One-Cancels-Other)
│   │   │   ├── 📁 retry/                  # Retry logic
│   │   │   │   ├── exponential_backoff.py # Exponential backoff
│   │   │   │   └── circuit_breaker.py     # Circuit breaker pattern
│   │   │   └── 📁 simulation/             # Execution simulation
│   │   │       ├── slippage_model.py      # Slippage simulation
│   │   │       └── fill_simulator.py      # Order fill simulation
│   │   │
│   │   ├── 📁 risk_management/            # Risk management system
│   │   │   ├── 📁 pre_trade/              # Pre-trade checks
│   │   │   │   ├── position_limit.py      # Position size limits
│   │   │   │   ├── exposure_limit.py      # Total exposure limits
│   │   │   │   ├── correlation_check.py   # Correlation entre positions
│   │   │   │   ├── capital_check.py       # Available capital
│   │   │   │   └── duplicate_order_check.py # Prevent duplicates (NUEVO)
│   │   │   ├── 📁 in_trade/               # In-trade monitoring
│   │   │   │   ├── stop_loss_manager.py   # Dynamic stop losses
│   │   │   │   ├── trailing_stop.py       # Trailing stops
│   │   │   │   └── time_exit.py           # Time-based exits
│   │   │   ├── 📁 portfolio/              # Portfolio-level risk
│   │   │   │   ├── var_calculator.py      # Value at Risk
│   │   │   │   ├── sharpe_monitor.py      # Real-time Sharpe
│   │   │   │   ├── beta_calculator.py     # Beta vs market
│   │   │   │   └── concentration.py       # Concentration risk
│   │   │   └── 📁 circuit_breakers/       # Emergency stops
│   │   │       ├── daily_loss_limit.py    # Max daily loss
│   │   │       ├── volatility_brake.py    # Extreme volatility
│   │   │       ├── latency_brake.py       # High latency detection
│   │   │       └── liquidation_brake.py   # Mass liquidation alert (NUEVO)
│   │   │
│   │   ├── 📁 backtesting/                # Backtesting engine
│   │   │   ├── 📁 engine/                 # Core backtesting
│   │   │   │   ├── backtest_engine.py     # Main backtest orchestrator
│   │   │   │   ├── event_processor.py     # Process historical events
│   │   │   │   └── state_manager.py       # Manage backtest state
│   │   │   ├── 📁 data/                   # Data handling
│   │   │   │   ├── data_loader.py         # Load historical data
│   │   │   │   ├── data_validator.py      # Validate data quality
│   │   │   │   └── resampler.py           # Resample timeframes
│   │   │   ├── 📁 simulation/             # Market simulation
│   │   │   │   ├── commission_model.py    # Commission simulation
│   │   │   │   ├── slippage_model.py      # Slippage model
│   │   │   │   └── market_impact.py       # Market impact model
│   │   │   ├── 📁 optimization/           # Parameter optimization
│   │   │   │   ├── grid_search.py         # Grid search optimizer
│   │   │   │   ├── genetic_algorithm.py   # GA optimizer
│   │   │   │   ├── walk_forward.py        # Walk-forward optimization
│   │   │   │   ├── monte_carlo.py         # Monte Carlo simulation (NUEVO)
│   │   │   │   └── multi_symbol_optimizer.py # Multi-symbol testing (NUEVO)
│   │   │   ├── 📁 metrics/                # Performance metrics
│   │   │   │   ├── returns.py             # Return calculations
│   │   │   │   ├── risk_metrics.py        # Sharpe, Sortino, Calmar
│   │   │   │   ├── drawdown.py            # Drawdown analysis
│   │   │   │   ├── trade_metrics.py       # Win rate, profit factor
│   │   │   │   └── survivorship_bias.py   # Bias detection (NUEVO)
│   │   │   └── 📁 validation/             # Validation (NUEVO)
│   │   │       ├── out_of_sample.py       # OOS validation
│   │   │       └── regime_specific.py     # Regime-specific testing
│   │   │
│   │   ├── 📁 portfolio/                  # Portfolio management
│   │   │   ├── portfolio_manager.py       # Main portfolio manager
│   │   │   ├── rebalancer.py              # Portfolio rebalancing
│   │   │   ├── allocator.py               # Capital allocation
│   │   │   └── performance_tracker.py     # Track performance
│   │   │
│   │   ├── 📁 alerting/                   # Alerting system
│   │   │   ├── 📁 channels/               # Alert channels
│   │   │   │   ├── telegram.py            # Telegram alerts
│   │   │   │   ├── discord.py             # Discord webhooks
│   │   │   │   ├── email.py               # Email alerts
│   │   │   │   └── sms.py                 # SMS alerts (Twilio)
│   │   │   ├── alert_manager.py           # Central alert manager
│   │   │   ├── rule_engine.py             # Alert rules
│   │   │   ├── escalation.py              # Alert escalation
│   │   │   └── liquidation_alerts.py      # Liquidation-specific alerts (NUEVO)
│   │   │
│   │   ├── 📁 infrastructure/             # Infrastructure layer
│   │   │   ├── 📁 exchanges/              # Exchange adapters
│   │   │   │   ├── base_exchange.py       # Base exchange interface
│   │   │   │   ├── binance_adapter.py     # Binance implementation
│   │   │   │   ├── hyperliquid_adapter.py # HyperLiquid (NUEVO)
│   │   │   │   ├── coinbase_adapter.py    # Coinbase
│   │   │   │   └── exchange_factory.py    # Factory pattern
│   │   │   ├── 📁 database/               # Database layer
│   │   │   │   ├── timescale_client.py    # TimescaleDB client
│   │   │   │   ├── redis_client.py        # Redis client
│   │   │   │   └── migrations/            # DB migrations
│   │   │   ├── 📁 message_bus/            # Message bus
│   │   │   │   ├── redis_streams.py       # Redis Streams impl
│   │   │   │   ├── publisher.py           # Event publisher
│   │   │   │   └── subscriber.py          # Event subscriber
│   │   │   ├── 📁 config/                 # Configuration
│   │   │   │   ├── settings.py            # Pydantic settings
│   │   │   │   ├── secrets.py             # Secrets management
│   │   │   │   └── environments/          # Env-specific configs
│   │   │   │       ├── development.yaml
│   │   │   │       ├── staging.yaml
│   │   │   │       └── production.yaml
│   │   │   └── 📁 logging/                # Logging setup
│   │   │       ├── logger.py              # Structured logging
│   │   │       ├── formatters.py          # Log formatters
│   │   │       └── handlers.py            # Log handlers
│   │   │
│   │   ├── 📁 monitoring/                 # Monitoring & observability (NUEVO)
│   │   │   ├── 📁 dashboards/
│   │   │   │   ├── terminal_dashboard.py  # Terminal-based dashboard
│   │   │   │   ├── web_dashboard.py       # Web dashboard
│   │   │   │   └── liquidations_monitor.py # Liquidations monitor
│   │   │   ├── metrics_collector.py       # Collect metrics
│   │   │   ├── health_checker.py          # System health checks
│   │   │   └── performance_profiler.py    # Performance profiling
│   │   │
│   │   ├── 📁 api/                        # REST API & WebSockets
│   │   │   ├── 📁 rest/                   # REST API
│   │   │   │   ├── main.py                # FastAPI app
│   │   │   │   ├── 📁 routers/            # API routers
│   │   │   │   │   ├── orders.py          # Orders endpoints
│   │   │   │   │   ├── positions.py       # Positions endpoints
│   │   │   │   │   ├── strategies.py      # Strategies endpoints
│   │   │   │   │   ├── backtests.py       # Backtesting endpoints
│   │   │   │   │   ├── scanner.py         # Scanner endpoints (NUEVO)
│   │   │   │   │   └── health.py          # Health check
│   │   │   │   ├── 📁 middleware/         # Middlewares
│   │   │   │   │   ├── auth.py            # Authentication
│   │   │   │   │   ├── rate_limit.py      # Rate limiting
│   │   │   │   │   └── cors.py            # CORS handling
│   │   │   │   └── 📁 schemas/            # Pydantic schemas
│   │   │   │       ├── order_schema.py
│   │   │   │       ├── strategy_schema.py
│   │   │   │       └── backtest_schema.py
│   │   │   └── 📁 websocket/              # WebSocket server
│   │   │       ├── server.py              # WS server
│   │   │       ├── handlers.py            # WS handlers
│   │   │       └── broadcaster.py         # Broadcast updates
│   │   │
│   │   └── 📁 cli/                        # Command-line tools
│   │       ├── main.py                    # Main CLI entry
│   │       ├── commands/
│   │       │   ├── start.py               # Start system
│   │       │   ├── stop.py                # Stop system
│   │       │   ├── backtest.py            # Run backtest
│   │       │   ├── scan.py                # Run scanner (NUEVO)
│   │       │   └── optimize.py            # Optimize params
│   │       └── utils.py
│   │
│   └── 📁 cpp/                            # C++ performance-critical components
│       ├── 📁 execution/                  # Execution engine (C++)
│       │   ├── order_executor.hpp/.cpp    # Ultra-low latency executor
│       │   ├── order_queue.hpp/.cpp       # Lock-free order queue
│       │   └── rate_limiter.hpp/.cpp      # Token bucket rate limiter
│       ├── 📁 market_data/                # Market data processing (C++)
│       │   ├── parser.hpp/.cpp            # Fast JSON/binary parser
│       │   ├── normalizer.hpp/.cpp        # Data normalization
│       │   └── circular_buffer.hpp/.cpp   # Lock-free circular buffer
│       ├── 📁 indicators/                 # Technical indicators (C++)
│       │   ├── sma.hpp/.cpp               # Simple Moving Average
│       │   ├── ema.hpp/.cpp               # Exponential MA
│       │   ├── rsi.hpp/.cpp               # RSI calculation
│       │   ├── macd.hpp/.cpp              # MACD calculation
│       │   └── bollinger.hpp/.cpp         # Bollinger Bands
│       ├── 📁 bindings/                   # Python bindings (pybind11)
│       │   ├── execution_bindings.cpp     # Execution bindings
│       │   ├── market_data_bindings.cpp   # Market data bindings
│       │   └── indicators_bindings.cpp    # Indicators bindings
│       └── CMakeLists.txt                 # CMake build config
│
├── 📁 tests/                              # Test suite
│   ├── 📁 unit/                           # Unit tests
│   │   ├── 📁 domain/
│   │   ├── 📁 strategies/
│   │   ├── 📁 risk_management/
│   │   ├── 📁 scanners/                   # (NUEVO)
│   │   └── 📁 execution/
│   ├── 📁 integration/                    # Integration tests
│   │   ├── test_market_data_flow.py
│   │   ├── test_execution_flow.py
│   │   ├── test_scanner_pipeline.py       # (NUEVO)
│   │   └── test_strategy_pipeline.py
│   ├── 📁 performance/                    # Performance tests
│   │   ├── test_latency.py
│   │   └── test_throughput.py
│   └── 📁 chaos/                          # Chaos engineering
│       ├── test_connection_loss.py
│       └── test_high_latency.py
│
├── 📁 config/                             # Configuration files
│   ├── development.yaml
│   ├── staging.yaml
│   ├── production.yaml
│   └── strategies/                        # Strategy configs
│       ├── rsi_macd.yaml
│       ├── breakout.yaml                  # (NUEVO - Moon Dev strategy)
│       ├── bollinger.yaml
│       └── grid_trading.yaml
│
├── 📁 data/                               # Data storage
│   ├── historical/                        # Historical data (CSV)
│   ├── backtests/                         # Backtest results
│   ├── scans/                             # Scanner results (NUEVO)
│   └── logs/                              # Application logs
│
├── 📁 scripts/                            # Utility scripts
│   ├── start.sh                           # Start system
│   ├── stop.sh                            # Stop system
│   ├── backup.sh                          # Backup data
│   ├── health_check.sh                    # Health check
│   ├── download_data.py                   # Download historical data
│   ├── run_scanner.py                     # Run market scanner (NUEVO)
│   └── optimize_strategy.py               # Strategy optimization
│
├── 📁 docker/                             # Docker configurations
│   ├── Dockerfile.python                  # Python service
│   ├── Dockerfile.cpp                     # C++ compilation
│   ├── docker-compose.yml                 # All services
│   └── docker-compose.dev.yml             # Development
│
├── 📁 docs/                               # Documentation
│   ├── architecture/                      # Architecture docs
│   │   ├── overview.md
│   │   ├── rbi_process.md                 # RBI process documentation (NUEVO)
│   │   ├── data_flow.md
│   │   └── diagrams/
│   ├── api/                               # API documentation
│   ├── strategies/                        # Strategy docs
│   │   └── breakout_strategy.md           # (NUEVO - Moon Dev)
│   └── deployment/                        # Deployment guides
│
├── 📁 monitoring/                         # Monitoring configs
│   ├── prometheus.yml                     # Prometheus config
│   ├── grafana/                           # Grafana dashboards
│   │   ├── system_health.json
│   │   ├── trading_metrics.json
│   │   ├── risk_metrics.json
│   │   └── liquidations_dashboard.json    # (NUEVO)
│   └── alerts/                            # Alert rules
│       └── alerting_rules.yml
│
├── 📁 notebooks/                          # Jupyter notebooks (NUEVO)
│   ├── research/                          # Research notebooks
│   │   ├── regime_analysis.ipynb
│   │   ├── strategy_exploration.ipynb
│   │   └── market_microstructure.ipynb
│   └── backtesting/                       # Backtest notebooks
│       ├── breakout_optimization.ipynb
│       └── multi_symbol_analysis.ipynb
│
├── .env.example                           # Environment variables template
├── .gitignore
├── README.md                              # Main documentation
├── CONTRIBUTING.md                        # Contribution guidelines
├── DEPLOYMENT.md                          # Deployment guide
├── RBI_CHECKLIST.md                       # RBI process checklist (NUEVO)
├── LICENSE
├── requirements.txt                       # Python dependencies
├── requirements-dev.txt                   # Development dependencies
├── setup.py                               # Python package setup
├── CMakeLists.txt                         # C++ build configuration
├── pyproject.toml                         # Python project metadata
└── Makefile                               # Build automation
```

---

## 🛠️ PARTE 2: STACK TECNOLÓGICO ÓPTIMO

### A) Lenguaje Principal - ARQUITECTURA HÍBRIDA

**DECISIÓN: Python 3.11+ + C++20** (NO negociable)

**Python para** (70% del código):
- Estrategias y lógica de negocio
- Backtesting y análisis (pandas, numpy, TA-Lib)
- Scanners y regime detection
- APIs y dashboards (FastAPI)
- Research y optimización

**C++ para** (30% del código):
- Order execution engine (<1ms latency)
- Market data parsing (millones de ticks/s)
- Indicadores técnicos en tiempo real
- Hot path crítico

**Integración**:
- **pybind11**: Binding principal
- Shared memory para latencia mínima

---

### B) Data Pipeline

**Recomendación Principal: Redis Streams**

**Justificación**:
- ✅ Latencia <5ms p99
- ✅ Simplicidad operacional
- ✅ Consumer groups
- ✅ Integración con cache

**Alternativas**:
1. **Kafka**: Mayor throughput, más complejo
2. **Pulsar**: Multi-tenancy, menos maduro

---

### C) Time-Series Database

**Recomendación: TimescaleDB**

**Justificación**:
- ✅ PostgreSQL extension (SQL familiar)
- ✅ Compresión 20x automática
- ✅ Continuous aggregates
- ✅ 10M+ inserts/s

**Alternativas**:
1. **QuestDB**: Performance extrema, menos maduro
2. **InfluxDB**: Específico para time-series, curva aprendizaje

---

### D) Backtesting Framework

**Recomendación: backtesting.py + Custom Extensions**

**Por qué** (basado en Moon Dev):
- ✅ Más rápido que Backtrader
- ✅ Vectorized operations
- ✅ Fácil optimización (grid search, walk-forward)
- ✅ Heat maps de resultados

**Implementación**:
```python
# Backtest con backtesting.py
from backtesting import Backtest, Strategy

class BreakoutStrategy(Strategy):
    # Moon Dev's proven strategy
    tp_percent = 0.07  # 7% take profit (optimizado)
    sl_percent = 0.16  # 16% stop loss (optimizado)
    
    def init(self):
        # Daily resistance (20-day SMA)
        self.daily_resistance = self.I(
            lambda: daily_data['high'].rolling(20).max()
        )
    
    def next(self):
        # Entry: hourly close > daily resistance
        if self.data.Close[-1] > self.daily_resistance[-1]:
            if not self.position:
                self.buy(
                    tp=self.data.Close[-1] * (1 + self.tp_percent),
                    sl=self.data.Close[-1] * (1 - self.sl_percent)
                )
```

---

### E) Exchange Connectors

**Recomendación: ccxt + Custom Wrappers**

**Exchanges prioritarios** (basado en Moon Dev):
1. **HyperLiquid**: Perpetuals DEX, low fees
2. **Binance**: Liquidez máxima
3. **Coinbase**: Institucional

---

### F) Monitoring Stack

**Recomendación: Terminal Dashboard + Prometheus + Grafana**

**Terminal Dashboard** (como Moon Dev):
```
┌──────────────────────────────────────────┐
│ 1. Scanner Results (breakouts detected) │
│ 2. Liquidations Feed (real-time)        │
│ 3. Open Positions                        │
│ 4. P&L Today                             │
│ 5. System Health                         │
│ 6. Recent Trades                         │
└──────────────────────────────────────────┘
```

---

## 🎯 PARTE 3: MÓDULOS CORE - IMPLEMENTACIÓN CRÍTICA

### 3.1 📊 SCANNER SYSTEM (NUEVO - CRÍTICO)

**Propósito**: Encontrar oportunidades automáticamente 24/7.

**Arquitectura**:
```python
# src/python/scanners/base/scanner.py
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

class Scanner(ABC):
    """Base scanner que todos los scanners deben implementar."""
    
    def __init__(self, symbols: List[str], timeframe: str):
        self.symbols = symbols
        self.timeframe = timeframe
        self.last_scan = None
    
    @abstractmethod
    async def scan(self) -> List[ScanResult]:
        """
        Escanea el mercado buscando oportunidades.
        
        Returns:
            Lista de ScanResult con símbolos que cumplen criterios
        """
        pass
    
    @abstractmethod
    def get_scan_criteria(self) -> dict:
        """Retorna criterios de escaneo para logging/debugging."""
        pass


# src/python/scanners/implementations/breakout_scanner.py
class BreakoutScanner(Scanner):
    """
    Scanner de breakouts (Moon Dev strategy).
    
    Busca símbolos donde:
    1. Precio actual > resistencia diaria (20-day high)
    2. Volumen confirmación
    3. No está en posición ya
    """
    
    def __init__(
        self,
        symbols: List[str],
        lookback_days: int = 20,
        min_volume_usd: float = 1_000_000
    ):
        super().__init__(symbols, timeframe="1h")
        self.lookback_days = lookback_days
        self.min_volume_usd = min_volume_usd
    
    async def scan(self) -> List[ScanResult]:
        results = []
        
        for symbol in self.symbols:
            # Fetch daily data
            daily_data = await self.fetch_daily_data(symbol, days=self.lookback_days)
            hourly_data = await self.fetch_hourly_data(symbol, hours=48)
            
            # Calculate resistance (20-day high)
            resistance = daily_data['high'].rolling(20).max().iloc[-1]
            
            # Current price (hourly close)
            current_price = hourly_data['close'].iloc[-1]
            
            # Volume check
            volume_24h_usd = hourly_data['volume'].iloc[-24:].sum()
            
            # Breakout condition
            if (current_price > resistance and 
                volume_24h_usd >= self.min_volume_usd):
                
                results.append(ScanResult(
                    symbol=symbol,
                    entry_price=current_price,
                    stop_loss=current_price * 0.84,  # 16% SL
                    take_profit=current_price * 1.07,  # 7% TP
                    resistance_level=resistance,
                    confidence=self._calculate_confidence(hourly_data),
                    scan_time=datetime.utcnow()
                ))
        
        self.last_scan = datetime.utcnow()
        return results
    
    def _calculate_confidence(self, data) -> float:
        """
        Calcula score de confianza (0-1) basado en:
        - Volumen
        - Momentum
        - Volatilidad
        """
        # Implementation...
        pass
```

**Uso**:
```python
# Escanear cada minuto
scanner = BreakoutScanner(
    symbols=exchange.get_all_symbols(),
    lookback_days=20,
    min_volume_usd=1_000_000
)

while True:
    results = await scanner.scan()
    
    for result in results:
        if result.confidence > 0.7:
            await place_order(result)
    
    await asyncio.sleep(60)  # Cada minuto
```

---

### 3.2 🚨 LIQUIDATIONS MONITOR (NUEVO - ALPHA GENERATOR)

**Propósito**: Trackear liquidaciones para identificar zonas de reversión.

**Implementación**:
```python
# src/python/market_data/feeds/liquidations_feed.py
import websocket
import json
from typing import Callable

class LiquidationsMonitor:
    """
    Monitor de liquidaciones en tiempo real.
    
    Conecta a Binance WebSocket para trackear:
    - Liquidaciones >$100k (importantes)
    - Liquidaciones >$1M (CRÍTICAS)
    - Clusters de liquidaciones
    """
    
    def __init__(self, min_size_usd: float = 100_000):
        self.min_size_usd = min_size_usd
        self.ws = None
        self.liquidation_zones = {}  # Track by price level
        
    async def connect(self):
        """Conecta a Binance liquidations stream."""
        self.ws = await websocket.connect(
            "wss://fstream.binance.com/ws/!forceOrder@arr"
        )
    
    async def stream_liquidations(
        self,
        callback: Callable
    ):
        """
        Stream liquidaciones en tiempo real.
        
        Args:
            callback: Function(liquidation) to call on cada liq
        """
        async for message in self.ws:
            data = json.loads(message)
            
            for liq in data['o']:
                size_usd = float(liq['q']) * float(liq['p'])
                
                if size_usd >= self.min_size_usd:
                    liquidation = Liquidation(
                        symbol=liq['s'],
                        side='long' if liq['S'] == 'SELL' else 'short',
                        price=float(liq['p']),
                        quantity_usd=size_usd,
                        timestamp=datetime.fromtimestamp(liq['T'] / 1000)
                    )
                    
                    # Track en zone
                    self._track_zone(liquidation)
                    
                    # Callback
                    await callback(liquidation)
    
    def _track_zone(self, liq: Liquidation):
        """
        Trackea zonas de liquidación.
        
        Si múltiples liquidations en mismo price level →
        zona importante de reversión potencial.
        """
        price_bucket = round(liq.price, -2)  # Round to nearest 100
        
        if price_bucket not in self.liquidation_zones:
            self.liquidation_zones[price_bucket] = {
                'total_usd': 0,
                'count': 0,
                'last_timestamp': None
            }
        
        zone = self.liquidation_zones[price_bucket]
        zone['total_usd'] += liq.quantity_usd
        zone['count'] += 1
        zone['last_timestamp'] = liq.timestamp
        
        # Alert si zona MASIVA
        if zone['total_usd'] > 5_000_000:  # >$5M liquidated
            await self.alert_massive_liquidation(price_bucket, zone)
```

**Uso**:
```python
# Monitor liquidaciones
monitor = LiquidationsMonitor(min_size_usd=100_000)

async def on_liquidation(liq: Liquidation):
    if liq.quantity_usd > 1_000_000:
        # MAJOR liquidation - mark level
        await mark_price_level(liq.price, 'liquidation_zone')
        await send_telegram_alert(
            f"🚨 ${liq.quantity_usd:,.0f} liquidated at {liq.price}"
        )

await monitor.stream_liquidations(callback=on_liquidation)
```

---

### 3.3 🎯 REGIME DETECTION (NUEVO - GAME CHANGER)

**8 Regímenes de Mercado** (Jim Simons):

```python
# src/python/regime_detection/regime_types.py
from enum import Enum

class MarketRegime(Enum):
    BULL_MARKET = "bull_market"
    BEAR_MARKET = "bear_market"
    RANGE_BOUND = "range_bound"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    ECONOMIC_BOOM = "economic_boom"
    ECONOMIC_RECESSION = "recession"
    CRISIS = "crisis"


# src/python/regime_detection/regime_classifier.py
class RegimeClassifier:
    """
    Clasifica el régimen actual del mercado.
    
    Usa features:
    - Volatilidad (VIX, ATR)
    - Trend (SMA slopes)
    - Volume patterns
    - Correlation structure
    """
    
    def __init__(self):
        self.features = FeatureExtractor()
        self.model = self._load_model()  # Pre-trained or rule-based
    
    async def classify_regime(self, market_data) -> MarketRegime:
        """
        Clasifica régimen actual.
        
        Returns:
            MarketRegime enum
        """
        features = self.features.extract(market_data)
        
        # Rule-based classification (o ML model)
        if features['volatility'] > 30:  # VIX > 30
            if features['trend_strength'] < -0.5:
                return MarketRegime.CRISIS
            return MarketRegime.HIGH_VOLATILITY
        
        if features['trend_slope'] > 0.5:
            return MarketRegime.BULL_MARKET
        elif features['trend_slope'] < -0.5:
            return MarketRegime.BEAR_MARKET
        else:
            return MarketRegime.RANGE_BOUND
    
    def get_optimal_strategies(
        self,
        regime: MarketRegime
    ) -> List[str]:
        """
        Retorna estrategias óptimas para régimen actual.
        
        Example:
            BULL_MARKET → ['breakout', 'momentum', 'trend_following']
            BEAR_MARKET → ['short_selling', 'mean_reversion']
            RANGE_BOUND → ['market_making', 'grid_trading']
        """
        strategy_map = {
            MarketRegime.BULL_MARKET: [
                'breakout',
                'momentum',
                'trend_following'
            ],
            MarketRegime.BEAR_MARKET: [
                'short_selling',
                'mean_reversion'
            ],
            MarketRegime.RANGE_BOUND: [
                'market_making',
                'grid_trading',
                'mean_reversion'
            ],
            MarketRegime.HIGH_VOLATILITY: [
                'volatility_arbitrage',
                'options_strategies'
            ],
            # ... otros regímenes
        }
        
        return strategy_map.get(regime, [])
```

---

### 3.4 🛡️ RISK MANAGEMENT - PRODUCTION HARDENED

**Pre-Trade Checks** (CRÍTICOS - aprendido de Moon Dev):

```python
# src/python/risk_management/pre_trade/comprehensive_validator.py

class OrderValidator:
    """
    Validación EXHAUSTIVA antes de cada orden.
    
    Moon Dev casi se liquida por saltarse esto.
    """
    
    async def validate_order(self, order: Order) -> ValidationResult:
        """
        Valida orden contra TODAS las reglas de riesgo.
        
        Returns:
            ValidationResult(valid=True/False, reasons=[...])
        """
        checks = [
            self._check_duplicate_order(order),
            self._check_position_exists(order),
            self._check_position_size_limit(order),
            self._check_leverage_limit(order),
            self._check_daily_loss_limit(order),
            self._check_correlation_risk(order),
            self._check_available_capital(order),
            self._check_sl_tp_valid(order),  # CRÍTICO
            self._check_price_decimals(order),  # CRÍTICO
            self._check_size_decimals(order),  # CRÍTICO
        ]
        
        results = await asyncio.gather(*checks)
        
        failed_checks = [r for r in results if not r.passed]
        
        if failed_checks:
            return ValidationResult(
                valid=False,
                reasons=[c.reason for c in failed_checks]
            )
        
        return ValidationResult(valid=True)
    
    async def _check_duplicate_order(self, order) -> CheckResult:
        """Previene duplicate orders (común bug)."""
        existing = await self.order_repo.get_open_orders(order.symbol)
        
        for existing_order in existing:
            if (existing_order.side == order.side and
                abs(existing_order.price - order.price) < 0.01):
                return CheckResult(
                    passed=False,
                    reason=f"Duplicate order detected: {existing_order.id}"
                )
        
        return CheckResult(passed=True)
    
    async def _check_sl_tp_valid(self, order) -> CheckResult:
        """
        CRÍTICO: Valida stop_loss < entry < take_profit.
        
        Moon Dev tuvo un bug aquí que casi lo liquida.
        """
        if order.stop_loss is None or order.take_profit is None:
            return CheckResult(
                passed=False,
                reason="Stop loss and take profit are MANDATORY"
            )
        
        if order.side == OrderSide.BUY:
            if not (order.stop_loss < order.price < order.take_profit):
                return CheckResult(
                    passed=False,
                    reason=f"Invalid SL/TP: {order.stop_loss} < {order.price} < {order.take_profit}"
                )
        
        # Similar check for SELL orders...
        
        return CheckResult(passed=True)
```

---

## 📦 PARTE 4: ENTREGABLES CON MOON DEV INSIGHTS

### 4.1 RBI_CHECKLIST.md (NUEVO)

```markdown
# RBI Process Checklist

## ✅ RESEARCH Phase (70% of time)

### Strategy Discovery
- [ ] Read 5+ academic papers on strategy type
- [ ] Study traders who use this strategy successfully
- [ ] Identify market regimes where strategy works
- [ ] Document hypothesis clearly

### Risk Assessment
- [ ] What can go wrong?
- [ ] Maximum theoretical loss?
- [ ] Black swan scenarios?

### Resources
- Google Scholar: [link]
- Trading books read: [list]
- Papers reviewed: [list]

---

## ✅ BACKTEST Phase (25% of time)

### Data Preparation
- [ ] Historical data downloaded (min 2 years)
- [ ] Data validated (no gaps, outliers handled)
- [ ] Multiple symbols selected (min 5)

### Initial Backtest
- [ ] Strategy coded in backtesting.py
- [ ] Commission model realistic (maker/taker)
- [ ] Slippage model included
- [ ] Run on Symbol 1: [results]
- [ ] Run on Symbol 2: [results]
- [ ] Run on Symbol 3: [results]

### Optimization
- [ ] Grid search on parameters
- [ ] Walk-forward optimization
- [ ] Heat maps generated
- [ ] Optimal parameters: [document]

### Validation
- [ ] Out-of-sample testing
- [ ] Different time periods tested
- [ ] Survivorship bias checked
- [ ] Results: [document]

### Acceptance Criteria
- [ ] Sharpe Ratio > 1.0
- [ ] Max Drawdown < 30%
- [ ] Win Rate > 40%
- [ ] Profit Factor > 1.5
- [ ] Works on 3+ symbols

---

## ✅ IMPLEMENT Phase (5% of time)

### Bot Development
- [ ] Scanner implemented
- [ ] Risk checks implemented
- [ ] Order execution tested
- [ ] Stop loss / take profit validated

### Paper Trading
- [ ] Run paper trading 1 week
- [ ] Results match backtest? [Y/N]
- [ ] Bugs found and fixed: [list]

### Live Trading (TINY SIZE)
- [ ] Start with $10-$50 position size
- [ ] Run 1 week
- [ ] Monitor 4x per day
- [ ] Results: [document]

### Scale Up
- [ ] Week 1: $10 → Results: [x]
- [ ] Week 2: $25 → Results: [x]
- [ ] Week 3: $50 → Results: [x]
- [ ] Week 4: $100 → Results: [x]

---

## 🚨 RED FLAGS (STOP IMMEDIATELY)

- [ ] Live results differ significantly from backtest
- [ ] Max drawdown exceeded
- [ ] Multiple technical failures
- [ ] Emotional stress trading

---

## 📊 Performance Tracking

| Week | Position Size | Trades | Win Rate | P&L | Notes |
|------|--------------|--------|----------|-----|-------|
| 1    | $10          |        |          |     |       |
| 2    | $25          |        |          |     |       |
| 3    | $50          |        |          |     |       |
```

---

### 4.2 Breakout Strategy Documentation (Moon Dev Validated)

```markdown
# Breakout Strategy (Daily Resistance / Hourly Entry)

## Strategy Overview
**Validated by Moon Dev** - 197% return on INJ backtest vs 71% buy-and-hold.

## Logic
1. Calculate daily resistance (20-day high)
2. Wait for hourly close above resistance
3. Enter long with:
   - Entry: Current hourly close
   - Take Profit: +7% (optimized via heat map)
   - Stop Loss: -16% (optimized via heat map)

## Backtest Results

### Symbol: INJ (Primary validation)
- Period: 208 days
- Return: 197%
- Buy & Hold: 71%
- Trades: 14
- Win Rate: 78%
- Max Drawdown: 31%
- Sharpe Ratio: 1.2

### Symbol: SOL
- Return: 452%
- Buy & Hold: 297%
- Trades: 22
- Win Rate: 73%

### Symbol: WHIFF (Survivorship bias - use caution)
- Return: 21,876%
- Buy & Hold: 1,255%
- **Note**: Likely overfit, token mooned

## Optimization Process
- Grid search: TP (3-20%), SL (3-20%)
- 400+ parameter combinations tested
- Heat map analysis revealed optimal: TP=7%, SL=16%

## Risk Controls
- **MANDATORY**: Position check before entry
- **MANDATORY**: Cancel pending orders before new order
- Position size: Start $10, scale to $50 max
- Max leverage: 3x
- Daily loss limit: -5%

## Implementation Notes
1. Run scanner every 60 seconds
2. Only enter if NO existing position
3. Price and size decimals validated
4. Orders require SL + TP (no exceptions)

## Known Issues
- Performs poorly in range-bound markets
- Requires volatility to work
- Not tested in bear market

## Next Steps
- [ ] Test in bear market regime
- [ ] Add regime filter (only run in bull)
- [ ] Test with different lookback periods (10-day, 30-day)
```

---

## 🎯 CRITERIOS DE ÉXITO ACTUALIZADOS

Tu implementación será exitosa si:

✅ Sistema corriendo en <10 minutos (git clone → docker-compose up)
✅ Backtest de 1 año en <5 minutos
✅ Scanner encuentra breakouts en tiempo real
✅ Liquidations monitor funciona 24/7
✅ Risk checks previenen liquidación
✅ **RBI process documented and followed**
✅ **Trades reales con $10 funcionan**
✅ Logs permiten debug completo
✅ Junior puede entender el código
✅ Escala a 100+ símbolos

---

## 🚨 CONSTRAINTS ACTUALIZADOS

### Hard Requirements (Moon Dev Validated):
- ⚠️ **NUNCA** skip backtesting phase
- ⚠️ **NUNCA** tradear sin stop loss + take profit
- ⚠️ **SIEMPRE** empezar con $10-$50 positions
- ⚠️ **SIEMPRE** validar decimals (price + size)
- ⚠️ **SIEMPRE** check if already in position
- ⚠️ **SIEMPRE** cancel pending orders before new
- ⚠️ **NUNCA** hardcodear credenciales
- ⚠️ **NUNCA** usar blocking I/O en hot path

### Performance Targets:
- Scanner: Scan 100+ symbols en <30 seconds
- Order placement: <50ms p99
- Market data: 10k+ updates/s
- Backtest: 1 año en <5 minutos
- Memory: <4GB para 100 símbolos

---

## 📚 LEARNING RESOURCES (Moon Dev Recommended)

### Books
- **Rob Carver** - "Advanced Futures Trading Strategies"
- Market regime analysis books
- Jim Simons / Renaissance Technologies studies

### Online
- Google Scholar (academic papers)
- YouTube (trading strategies)
- Baby Pips (Forex basics)

### Practice
- Paper trading 1 week minimum
- Start with $10 real money
- Scale slowly based on results

---

## 🗺️ ROADMAP

### V1.0 (MVP - Week 1-2)
- ✅ Exchange connector (HyperLiquid)
- ✅ Breakout strategy (Moon Dev validated)
- ✅ Basic backtesting
- ✅ Scanner system
- ✅ Risk management basics

### V1.5 (Production - Week 3-4)
- ✅ Liquidations monitor
- ✅ Regime detection
- ✅ Multi-symbol backtesting
- ✅ Terminal dashboard
- ✅ Advanced risk controls

### V2.0 (Institutional - Month 2)
- ✅ C++ hot path
- ✅ ML regime classifier
- ✅ Auto-optimization
- ✅ Multi-exchange
- ✅ Portfolio management

---

**NOTA FINAL**: 

Este prompt incorpora **3.5 años de experiencia** de Moon Dev en producción. No es teoría - es código que mueve dinero real.

**Prioridad #1**: CONFIABILIDAD > Features fancy.

**Recuerda**: El código debe ser tan bueno que lo usarías con tu propio dinero. Porque lo harás. 💰