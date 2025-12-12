# 🗺️ ROADMAP ULTRA-DETALLADO: SISTEMA DE TRADING ALGORÍTMICO INSTITUCIONAL

Voy a crear un roadmap **extremadamente detallado** que divide el proyecto en sprints manejables, con dependencias claras y criterios de aceptación específicos.

---

## 📊 VISIÓN GENERAL DEL ROADMAP

```
FASE 0: Setup & Foundation (3-5 días)
   ↓
FASE 1: Core Infrastructure (1-2 semanas)
   ↓
FASE 2: Market Data Engine (1 semana)
   ↓
FASE 3: Strategy Framework (1 semana)
   ↓
FASE 4: Backtesting System (1-2 semanas)
   ↓
FASE 5: Scanner System (1 semana)
   ↓
FASE 6: Risk Management (1 semana)
   ↓
FASE 7: Execution Engine (1 semana)
   ↓
FASE 8: Monitoring & Alerts (3-5 días)
   ↓
FASE 9: Production Hardening (1 semana)
   ↓
FASE 10: Advanced Features (ongoing)
```

**Total estimado MVP**: 8-10 semanas
**Total Production-Ready**: 12-14 semanas

---

## 🎯 FASE 0: SETUP & FOUNDATION (Días 1-3)

### **Sprint 0.1: Environment Setup**
**Duración**: 4-6 horas

#### Tareas:
1. **Crear estructura base del proyecto**
   - [ ] Inicializar repositorio Git
   - [ ] Crear estructura de carpetas completa (según prompt)
   - [ ] Setup .gitignore (secrets, __pycache__, venv)
   - [ ] Crear README.md inicial

2. **Python Environment**
   - [ ] Setup Python 3.11+ (pyenv recomendado)
   - [ ] Crear virtualenv
   - [ ] Instalar dependencias base:
     ```
     # requirements.txt inicial
     fastapi==0.104.1
     uvicorn==0.24.0
     pydantic==2.5.0
     pydantic-settings==2.1.0
     asyncio==3.4.3
     aiohttp==3.9.1
     websockets==12.0
     ccxt==4.1.0
     pandas==2.1.4
     numpy==1.26.2
     ta-lib==0.4.28
     backtesting==0.3.3
     redis==5.0.1
     psycopg2-binary==2.9.9
     python-telegram-bot==20.7
     python-dotenv==1.0.0
     pytest==7.4.3
     pytest-asyncio==0.21.1
     ```

3. **Docker Setup**
   - [ ] Crear Dockerfile.python
   - [ ] Crear docker-compose.yml con servicios:
     - PostgreSQL (TimescaleDB)
     - Redis
     - Grafana (opcional en MVP)
   - [ ] Verificar docker-compose up funciona

4. **Config Management**
   - [ ] Crear .env.example con todas las variables
   - [ ] Implementar settings.py con Pydantic Settings
   - [ ] Crear configs por ambiente (dev/staging/prod)

**Criterios de Aceptación**:
- ✅ `docker-compose up` levanta todos los servicios
- ✅ Python environment funciona sin errores
- ✅ Estructura de carpetas completa creada
- ✅ Git configurado con .gitignore correcto

**Entregables**:
- Repositorio Git inicializado
- Docker funcionando
- Python environment listo
- Settings management implementado

---

### **Sprint 0.2: Domain Layer Foundation**
**Duración**: 6-8 horas

#### Tareas:
1. **Value Objects** (`domain/value_objects/`)
   - [ ] `symbol.py`: TradingPair class
     ```python
     @dataclass(frozen=True)
     class TradingPair:
         base: str
         quote: str
         exchange: str
         
         def __str__(self) -> str:
             return f"{self.base}/{self.quote}"
     ```
   
   - [ ] `money.py`: Money class (Decimal-based)
   - [ ] `timeframe.py`: Timeframe enum (1m, 5m, 1h, etc.)
   - [ ] `price.py`: Price class con precision

2. **Core Entities** (`domain/entities/`)
   - [ ] `order.py`: 
     - OrderType (MARKET, LIMIT, STOP_LOSS, etc.)
     - OrderSide (BUY, SELL)
     - OrderStatus (PENDING, FILLED, CANCELLED, etc.)
     - Order entity
   
   - [ ] `trade.py`: Trade execution record
   - [ ] `position.py`: Position tracking
   - [ ] `candle.py`: OHLCV candle entity
   - [ ] `signal.py`: Trading signal entity

3. **Repository Interfaces** (`domain/repositories/`)
   - [ ] `order_repository.py`: Interface abstracta
   - [ ] `trade_repository.py`: Interface abstracta
   - [ ] `candle_repository.py`: Interface abstracta

4. **Domain Events** (`domain/events/`)
   - [ ] `order_events.py`: OrderCreated, OrderFilled, OrderCancelled
   - [ ] `trade_events.py`: TradeExecuted, TradeRejected
   - [ ] Event base class

**Criterios de Aceptación**:
- ✅ Todas las clases son inmutables donde corresponda
- ✅ Value objects implementan __eq__ y __hash__
- ✅ Entities tienen IDs únicos
- ✅ Zero dependencias externas en domain layer
- ✅ Unit tests para cada value object/entity

**Entregables**:
- Domain layer completo y testeado
- 20+ unit tests pasando
- Documentación inline en cada clase

---

## 🏗️ FASE 1: CORE INFRASTRUCTURE (Semana 1-2)

### **Sprint 1.1: Database Layer**
**Duración**: 2-3 días

#### Tareas:
1. **TimescaleDB Setup**
   - [ ] Crear schema inicial:
     ```sql
     -- candles table (hypertable)
     CREATE TABLE candles (
         time TIMESTAMPTZ NOT NULL,
         symbol TEXT NOT NULL,
         timeframe TEXT NOT NULL,
         open DECIMAL NOT NULL,
         high DECIMAL NOT NULL,
         low DECIMAL NOT NULL,
         close DECIMAL NOT NULL,
         volume DECIMAL NOT NULL
     );
     SELECT create_hypertable('candles', 'time');
     
     -- orders table
     CREATE TABLE orders (...);
     
     -- trades table
     CREATE TABLE trades (...);
     ```
   
   - [ ] Implementar migraciones con Alembic
   - [ ] Crear continuous aggregates para 15m, 1h, 4h, 1d

2. **Repository Implementations** (`infrastructure/database/`)
   - [ ] `timescale_client.py`: Cliente TimescaleDB
   - [ ] `order_repository_impl.py`: Implementación concreta
   - [ ] `trade_repository_impl.py`
   - [ ] `candle_repository_impl.py`
   - [ ] Connection pooling
   - [ ] Error handling y retries

3. **Redis Setup** (`infrastructure/database/`)
   - [ ] `redis_client.py`: Cliente Redis con connection pool
   - [ ] Implementar cache patterns:
     - Latest candles (TTL 1 min)
     - Active orders (TTL on fill)
     - Market data snapshots

**Criterios de Aceptación**:
- ✅ TimescaleDB acepta 10k+ inserts/s
- ✅ Redis cache hit rate >80% en reads
- ✅ Migrations funcionan forward/backward
- ✅ Connection pooling maneja 100+ connections
- ✅ Integration tests con DB real

**Entregables**:
- DB schema versionado
- Repositories implementados
- Redis cache funcionando
- 15+ integration tests

---

### **Sprint 1.2: Exchange Connector Foundation**
**Duración**: 3-4 días

#### Tareas:
1. **Base Exchange Interface** (`infrastructure/exchanges/`)
   - [ ] `base_exchange.py`: Abstract interface
     ```python
     class BaseExchange(ABC):
         @abstractmethod
         async def get_balance(self) -> Dict
         
         @abstractmethod
         async def place_order(self, order: Order) -> str
         
         @abstractmethod
         async def cancel_order(self, order_id: str)
         
         @abstractmethod
         async def get_open_orders(self) -> List[Order]
         
         @abstractmethod
         async def subscribe_trades(self, symbol: str)
     ```

2. **CCXT Integration**
   - [ ] Wrapper sobre CCXT con:
     - Retry logic (exponential backoff)
     - Rate limiting (token bucket)
     - Error normalization
     - Decimal precision handling

3. **Binance Adapter** (`infrastructure/exchanges/binance_adapter.py`)
   - [ ] REST API implementation
   - [ ] WebSocket para market data (trades, orderbook)
   - [ ] WebSocket para user data (orders, positions)
   - [ ] Signature authentication
   - [ ] Handle Binance-specific quirks

4. **HyperLiquid Adapter** (opcional en MVP)
   - [ ] Similar a Binance
   - [ ] Manejar diferencias en API

**Criterios de Aceptación**:
- ✅ Place order funciona (testnet)
- ✅ Cancel order funciona
- ✅ WebSocket reconecta automáticamente
- ✅ Rate limiting previene bans
- ✅ Maneja 429 errors gracefully
- ✅ Decimals validados para cada symbol

**Entregables**:
- BaseExchange interface completa
- Binance adapter funcionando en testnet
- Rate limiter implementado
- 10+ integration tests (con testnet)

---

### **Sprint 1.3: Message Bus & Event System**
**Duración**: 2 días

#### Tareas:
1. **Redis Streams Implementation** (`infrastructure/message_bus/`)
   - [ ] `redis_streams.py`: Cliente Redis Streams
   - [ ] `publisher.py`: Publish events
   - [ ] `subscriber.py`: Subscribe to streams con consumer groups
   - [ ] Stream names:
     - `market_data:candles`
     - `market_data:trades`
     - `orders:events`
     - `trades:events`
     - `signals:generated`

2. **Event Bus Pattern**
   - [ ] Event dispatcher
   - [ ] Event handlers registry
   - [ ] Async event processing
   - [ ] Dead letter queue para failed events

3. **Domain Events Integration**
   - [ ] Conectar domain events → Redis Streams
   - [ ] Replay capability para debugging

**Criterios de Aceptación**:
- ✅ Maneja 1000+ events/s
- ✅ Consumer groups funcionan correctamente
- ✅ Failed events van a DLQ
- ✅ Event replay funciona
- ✅ <5ms p99 latency

**Entregables**:
- Message bus funcionando
- Event system integrado
- Performance tests pasando

---

## 📡 FASE 2: MARKET DATA ENGINE (Semana 3)

### **Sprint 2.1: Market Data Feeds**
**Duración**: 3-4 días

#### Tareas:
1. **Base Feed Interface** (`market_data/feeds/base_feed.py`)
   - [ ] Abstract feed class
   - [ ] Connection management
   - [ ] Reconnection logic
   - [ ] Data validation

2. **Binance WebSocket Feed** (`market_data/feeds/binance_feed.py`)
   - [ ] Subscribe to trades stream
   - [ ] Subscribe to orderbook stream
   - [ ] Subscribe to klines (candles) stream
   - [ ] Parse y normalize data
   - [ ] Handle connection drops
   - [ ] Emit events to Redis Streams

3. **Data Processors** (`market_data/processors/`)
   - [ ] `normalizer.py`: Normalize entre exchanges
   - [ ] `validator.py`: Validate data integrity
     - Timestamp checks
     - Price sanity checks
     - Volume outliers
   - [ ] `gap_detector.py`: Detect missing data
   - [ ] `aggregator.py`: Aggregate multi-timeframes

4. **Storage Layer** (`market_data/storage/`)
   - [ ] `timeseries_writer.py`: Batch writes a TimescaleDB
   - [ ] `cache_manager.py`: Write to Redis cache
   - [ ] Buffer management (flush every 1s o 1000 candles)

**Criterios de Aceptación**:
- ✅ Procesa 10k+ market updates/s
- ✅ Reconexión automática en <5s
- ✅ Data gaps detectados y logged
- ✅ Buffer flush no bloquea main loop
- ✅ Memory usage estable (<500MB para 10 symbols)

**Entregables**:
- Market data pipeline funcionando end-to-end
- Data fluyendo a DB y cache
- Monitoring de data quality
- 15+ tests

---

### **Sprint 2.2: Historical Data & Replay**
**Duración**: 2 días

#### Tareas:
1. **Data Downloader** (`scripts/download_data.py`)
   - [ ] Descargar historical candles desde Binance API
   - [ ] Support multiple symbols
   - [ ] Support multiple timeframes
   - [ ] Resume capability (partial downloads)
   - [ ] Progress bar
   - [ ] Validate downloaded data

2. **Data Storage**
   - [ ] Save to CSV (`data/historical/`)
   - [ ] Save to TimescaleDB
   - [ ] Compression (TimescaleDB compression)

3. **Replay Engine** (`market_data/replay/`)
   - [ ] `replay_engine.py`: Replay historical data
   - [ ] Speed control (1x, 10x, 100x)
   - [ ] Emit events como si fueran real-time
   - [ ] Progress tracking

**Criterios de Aceptación**:
- ✅ Descarga 2 años de data en <10 min
- ✅ Replay funciona a diferentes speeds
- ✅ Data integrity mantenida
- ✅ CSV export funciona

**Entregables**:
- Script de descarga funcionando
- 2+ años de data para BTC, ETH, SOL, etc.
- Replay engine implementado

---

## 🎯 FASE 3: STRATEGY FRAMEWORK (Semana 4)

### **Sprint 3.1: Strategy Base Classes**
**Duración**: 2 días

#### Tareas:
1. **Base Strategy** (`strategies/base/strategy.py`)
   ```python
   class Strategy(ABC):
       def __init__(self, config: StrategyConfig):
           self.config = config
           self.positions = {}
           self.indicators = {}
       
       @abstractmethod
       def on_candle(self, candle: Candle) -> List[Signal]:
           """Called on each new candle"""
           pass
       
       @abstractmethod
       def on_trade(self, trade: Trade):
           """Called on each trade"""
           pass
       
       def calculate_position_size(self, signal: Signal) -> Decimal:
           """Calculate position size based on risk"""
           pass
   ```

2. **Indicator Protocol** (`strategies/base/indicator.py`)
   - [ ] Abstract indicator interface
   - [ ] Caching mechanism
   - [ ] Vectorized computation support

3. **Signal Generation** (`strategies/base/signal.py`)
   - [ ] Signal class with confidence score
   - [ ] Signal validation
   - [ ] Signal filtering

**Criterios de Aceptación**:
- ✅ Base classes son extensibles
- ✅ Position sizing integrado
- ✅ Indicators son cacheables
- ✅ Signals tienen metadata completa

---

### **Sprint 3.2: Breakout Strategy Implementation**
**Duración**: 3 días

#### Tareas:
1. **Strategy Implementation** (`strategies/momentum/breakout.py`)
   ```python
   class BreakoutStrategy(Strategy):
       """
       Moon Dev's validated breakout strategy.
       
       Logic:
       1. Calculate daily resistance (20-day high)
       2. Wait for hourly close > resistance
       3. Enter with 7% TP, 16% SL
       """
       
       def __init__(self, config):
           super().__init__(config)
           self.lookback_days = config.lookback_days  # 20
           self.tp_percent = config.tp_percent  # 0.07
           self.sl_percent = config.sl_percent  # 0.16
       
       def on_candle(self, candle: Candle) -> List[Signal]:
           # Get daily data
           daily_data = self.get_daily_candles(candle.symbol, self.lookback_days)
           
           # Calculate resistance
           resistance = daily_data['high'].rolling(20).max().iloc[-1]
           
           # Check breakout
           if candle.close > resistance:
               return [Signal(
                   symbol=candle.symbol,
                   side=OrderSide.BUY,
                   entry_price=candle.close,
                   stop_loss=candle.close * (1 - self.sl_percent),
                   take_profit=candle.close * (1 + self.tp_percent),
                   confidence=self._calculate_confidence(candle, daily_data)
               )]
           
           return []
   ```

2. **Configuration** (`config/strategies/breakout.yaml`)
   ```yaml
   strategy:
     name: breakout
     type: momentum
     
   parameters:
     lookback_days: 20
     tp_percent: 0.07
     sl_percent: 0.16
     min_volume_usd: 1000000
     
   risk:
     max_position_size_usd: 1000
     max_positions: 3
   ```

3. **Testing**
   - [ ] Unit tests para logic
   - [ ] Integration test con historical data
   - [ ] Validate signals generated

**Criterios de Aceptación**:
- ✅ Strategy genera signals correctos
- ✅ TP/SL calculados correctamente
- ✅ Works con historical data
- ✅ Configurable via YAML

**Entregables**:
- Breakout strategy implementada
- Config files
- 10+ unit tests
- Strategy documentation

---

## 🧪 FASE 4: BACKTESTING SYSTEM (Semana 5-6)

### **Sprint 4.1: Backtesting Engine Core**
**Duración**: 4-5 días

#### Tareas:
1. **Backtest Engine** (`backtesting/engine/backtest_engine.py`)
   ```python
   class BacktestEngine:
       """
       Main backtesting orchestrator.
       """
       
       def __init__(
           self,
           strategy: Strategy,
           data: pd.DataFrame,
           initial_capital: Decimal,
           commission: Decimal = Decimal('0.001')
       ):
           self.strategy = strategy
           self.data = data
           self.portfolio = Portfolio(initial_capital)
           self.commission_model = CommissionModel(commission)
       
       async def run(self) -> BacktestResult:
           """Run backtest"""
           for i, candle in enumerate(self.data.itertuples()):
               # Generate signals
               signals = self.strategy.on_candle(candle)
               
               # Execute signals
               for signal in signals:
                   self._execute_signal(signal)
               
               # Update positions
               self._update_positions(candle)
           
           return self._calculate_results()
   ```

2. **Simulation Components** (`backtesting/simulation/`)
   - [ ] `commission_model.py`: Maker/taker fees
   - [ ] `slippage_model.py`: Realistic slippage
   - [ ] `market_impact.py`: Price impact on large orders
   - [ ] `fill_simulator.py`: Simulate order fills

3. **State Management** (`backtesting/engine/state_manager.py`)
   - [ ] Portfolio state tracking
   - [ ] Position tracking
   - [ ] Order history
   - [ ] Trade history

4. **Data Loading** (`backtesting/data/`)
   - [ ] Load from CSV
   - [ ] Load from TimescaleDB
   - [ ] Data validation
   - [ ] Resampling para multiple timeframes

**Criterios de Aceptación**:
- ✅ Backtest 1 año en <5 min (100k candles)
- ✅ Results match manual calculation
- ✅ Commission/slippage aplicados correctamente
- ✅ Memory usage <2GB para 1 año

---

### **Sprint 4.2: Performance Metrics & Reporting**
**Duración**: 2-3 días

#### Tareas:
1. **Metrics Calculation** (`backtesting/metrics/`)
   - [ ] `returns.py`:
     - Total return
     - Annualized return
     - Monthly returns
   
   - [ ] `risk_metrics.py`:
     - Sharpe ratio
     - Sortino ratio
     - Calmar ratio
     - Max drawdown
     - Volatility
   
   - [ ] `trade_metrics.py`:
     - Win rate
     - Profit factor
     - Average win/loss
     - Expectancy
     - Trade duration

   - [ ] `drawdown.py`:
     - Drawdown curve
     - Underwater plot
     - Recovery time

2. **Result Visualization**
   - [ ] Equity curve plot
   - [ ] Drawdown plot
   - [ ] Monthly returns heatmap
   - [ ] Trade distribution
   - [ ] Entry/exit markers on price chart

3. **Report Generation**
   - [ ] HTML report con plots
   - [ ] CSV export de trades
   - [ ] JSON summary

**Criterios de Aceptación**:
- ✅ Sharpe calculado correctamente
- ✅ Drawdown coincide con equity curve
- ✅ Reports son readable y útiles
- ✅ Can export to multiple formats

**Entregables**:
- Metrics library completa
- Report generator
- Sample reports

---

### **Sprint 4.3: Optimization Framework**
**Duración**: 3-4 días

#### Tareas:
1. **Grid Search** (`backtesting/optimization/grid_search.py`)
   ```python
   optimizer = GridSearchOptimizer(
       strategy=BreakoutStrategy,
       data=historical_data,
       param_grid={
           'tp_percent': np.arange(0.03, 0.20, 0.01),
           'sl_percent': np.arange(0.03, 0.20, 0.01),
           'lookback_days': [10, 15, 20, 25, 30]
       }
   )
   
   results = optimizer.optimize(
       objective='sharpe_ratio',
       n_jobs=8  # Parallel
   )
   ```

2. **Walk-Forward Optimization** (`backtesting/optimization/walk_forward.py`)
   - [ ] Split data en train/test windows
   - [ ] Optimize en train, validate en test
   - [ ] Rolling window approach
   - [ ] Anchored window approach

3. **Multi-Symbol Testing** (`backtesting/optimization/multi_symbol_optimizer.py`)
   - [ ] Test strategy en 5+ symbols
   - [ ] Aggregate results
   - [ ] Detect overfitting (works on 1 symbol only)

4. **Visualization**
   - [ ] Heat map de optimization results
   - [ ] Parameter sensitivity analysis
   - [ ] Walk-forward equity curves

**Criterios de Aceptación**:
- ✅ Grid search 400+ combinations en <30 min
- ✅ Walk-forward funcionando correctamente
- ✅ Multi-symbol results aggregated
- ✅ Heat maps generados
- ✅ Parallel processing funciona

**Entregables**:
- Optimization framework completo
- Heat map generator
- Walk-forward implementation
- Sample optimization runs

---

## 🔍 FASE 5: SCANNER SYSTEM (Semana 7)

### **Sprint 5.1: Scanner Framework**
**Duración**: 2-3 días

#### Tareas:
1. **Base Scanner** (`scanners/base/scanner.py`)
   ```python
   class Scanner(ABC):
       def __init__(self, symbols: List[str], config: ScannerConfig):
           self.symbols = symbols
           self.config = config
           self.last_scan = None
       
       @abstractmethod
       async def scan(self) -> List[ScanResult]:
           """Scan market for opportunities"""
           pass
       
       @abstractmethod
       def get_criteria(self) -> Dict:
           """Return scan criteria"""
           pass
   ```

2. **Scanner Result** (`scanners/base/scanner_result.py`)
   ```python
   @dataclass
   class ScanResult:
       symbol: str
       entry_price: Decimal
       stop_loss: Decimal
       take_profit: Decimal
       confidence: float  # 0-1
       scan_time: datetime
       metadata: Dict  # Additional info
   ```

3. **Scanner Engine** (`scanners/scanner_engine.py`)
   - [ ] Orchestrate multiple scanners
   - [ ] Schedule scans
   - [ ] Aggregate results
   - [ ] Filter duplicates
   - [ ] Rank by confidence

**Criterios de Aceptación**:
- ✅ Scanner interface es extensible
- ✅ Results son consistentes
- ✅ Engine maneja múltiples scanners

---

### **Sprint 5.2: Breakout Scanner Implementation**
**Duración**: 2 días

#### Tareas:
1. **Breakout Scanner** (`scanners/implementations/breakout_scanner.py`)
   ```python
   class BreakoutScanner(Scanner):
       """
       Scan for breakouts above daily resistance.
       """
       
       async def scan(self) -> List[ScanResult]:
           results = []
           
           for symbol in self.symbols:
               # Fetch data
               daily_data = await self.fetch_daily(symbol, days=20)
               hourly_data = await self.fetch_hourly(symbol, hours=48)
               
               # Calculate resistance
               resistance = daily_data['high'].rolling(20).max().iloc[-1]
               current = hourly_data['close'].iloc[-1]
               
               # Check breakout
               if current > resistance:
                   results.append(ScanResult(
                       symbol=symbol,
                       entry_price=current,
                       stop_loss=current * 0.84,
                       take_profit=current * 1.07,
                       confidence=self._calc_confidence(hourly_data),
                       scan_time=datetime.utcnow()
                   ))
           
           return results
   ```

2. **Volume Scanner** (bonus)
   - [ ] Scan for volume spikes
   - [ ] Detect unusual activity

3. **CLI Tool** (`scripts/run_scanner.py`)
   ```bash
   python scripts/run_scanner.py \
       --scanner breakout \
       --symbols BTC/USDT,ETH/USDT,SOL/USDT \
       --interval 60
   ```

**Criterios de Aceptación**:
- ✅ Scanner 100+ symbols en <30s
- ✅ Finds breakouts correctamente
- ✅ Confidence score es útil
- ✅ CLI tool funciona

**Entregables**:
- Scanner framework completo
- Breakout scanner implementado
- CLI tool
- 10+ tests

---

## 🛡️ FASE 6: RISK MANAGEMENT (Semana 8)

### **Sprint 6.1: Pre-Trade Validation**
**Duración**: 3 días

#### Tareas:
1. **Order Validator** (`risk_management/pre_trade/comprehensive_validator.py`)
   ```python
   class OrderValidator:
       """
       CRITICAL: Validate ALL orders before execution.
       """
       
       async def validate(self, order: Order) -> ValidationResult:
           checks = [
               self._check_duplicate_order(order),
               self._check_existing_position(order),
               self._check_position_size_limit(order),
               self._check_leverage_limit(order),
               self._check_daily_loss_limit(order),
               self._check_sl_tp_mandatory(order),
               self._check_price_decimals(order),
               self._check_size_decimals(order),
               self._check_available_capital(order),
           ]
           
           results = await asyncio.gather(*checks)
           
           if any(not r.passed for r in results):
               return ValidationResult(
                   valid=False,
                   reasons=[r.reason for r in results if not r.passed]
               )
           
           return ValidationResult(valid=True)
   ```

2. **Individual Checks** (`risk_management/pre_trade/`)
   - [ ] `duplicate_order_check.py`
   - [ ] `position_limit.py`: Max position size
   - [ ] `exposure_limit.py`: Total exposure
   - [ ] `capital_check.py`: Available balance
   - [ ] `correlation_check.py`: Correlation risk

3. **Configuration**
   ```yaml
   risk_limits:
     max_position_size_usd: 1000
     max_total_exposure_usd: 5000
     max_positions: 3
     max_leverage: 3
     daily_loss_limit_percent: 5
     require_stop_loss: true
     require_take_profit: true
   ```

**Criterios de Aceptación**:
- ✅ Todos los checks implementados
- ✅ Invalid orders son rechazadas
- ✅ Error messages son claros
- ✅ <10ms validation time
- ✅ 20+ unit tests

---

### **Sprint 6.2: In-Trade Risk Management**
**Duración**: 2 días

#### Tareas:
1. **Stop Loss Manager** (`risk_management/in_trade/stop_loss_manager.py`)
   - [ ] Track open positions
   - [ ] Monitor SL levels
   - [ ] Execute SL orders
   - [ ] Trailing stop logic

2. **Circuit Breakers** (`risk_management/circuit_breakers/`)
   - [ ] `daily_loss_limit.py`: Stop trading si loss > 5%
   - [ ] `volatility_brake.py`: Pause en high volatility
   - [ ] `latency_brake.py`: Pause si latency >500ms
   - [ ] `connection_brake.py`: Pause si connection lost

3. **Portfolio Risk** (`risk_management/portfolio/`)
   - [ ] `var_calculator.py`: Value at Risk
   - [ ] `sharpe_monitor.py`: Real-time Sharpe
   - [ ] `concentration.py`: Position concentration

**Criterios de Aceptación**:
- ✅ Circuit breakers funcionan
- ✅ SL ejecutado automáticamente
- ✅ Portfolio risk calculado en real-time
- ✅ Sistema para trading si limits excedidos

**Entregables**:
- Risk management completo
- Circuit breakers funcionando
- 15+ tests

---

# ⚡ FASE 7: EXECUTION ENGINE (Semana 9)

## **Sprint 7.1: Order Execution Core**
**Duración**: 3-4 días

### Tareas:

#### 1. **Executor Core** (`execution/engine/executor.py`)
```python
# execution/engine/executor.py
from typing import Optional
from decimal import Decimal
import asyncio
from datetime import datetime

class OrderExecutor:
    """
    Execute orders with comprehensive validation and retry logic.
    
    CRITICAL: This is the money-making/losing component.
    Every line must be bulletproof.
    """
    
    def __init__(
        self,
        exchange_adapter: BaseExchange,
        validator: OrderValidator,
        risk_manager: RiskManager,
        alert_manager: AlertManager,
        order_repository: OrderRepository
    ):
        self.exchange = exchange_adapter
        self.validator = validator
        self.risk_manager = risk_manager
        self.alert_manager = alert_manager
        self.order_repo = order_repository
        self.retry_handler = ExponentialBackoff(max_retries=3)
        
    async def execute(self, order: Order) -> ExecutionResult:
        """
        Execute order with full validation pipeline.
        
        Steps:
        1. Pre-trade validation
        2. Cancel conflicting orders
        3. Check existing positions
        4. Execute with retry
        5. Monitor fill
        6. Update tracking
        
        Returns:
            ExecutionResult with order_id if success
        """
        try:
            # 1. PRE-TRADE VALIDATION (CRITICAL)
            validation = await self.validator.validate(order)
            if not validation.valid:
                await self.alert_manager.send_alert(
                    f"❌ Order rejected: {validation.reasons}",
                    priority=AlertPriority.HIGH
                )
                return ExecutionResult(
                    success=False,
                    error=f"Validation failed: {validation.reasons}"
                )
            
            # 2. CANCEL PENDING ORDERS (Moon Dev lesson)
            await self._cancel_pending_orders(order.symbol)
            
            # 3. CHECK EXISTING POSITION (prevent duplicates)
            if await self._has_position(order.symbol):
                return ExecutionResult(
                    success=False,
                    error=f"Already in position for {order.symbol}"
                )
            
            # 4. NORMALIZE ORDER (decimals, precision)
            normalized_order = await self._normalize_order(order)
            
            # 5. EXECUTE WITH RETRY
            execution_result = await self._execute_with_retry(normalized_order)
            
            if execution_result.success:
                # 6. TRACK ORDER
                await self.order_repo.save(normalized_order)
                
                # 7. ALERT SUCCESS
                await self.alert_manager.send_alert(
                    f"✅ Order placed: {order.symbol} {order.side} "
                    f"@ {order.price} (ID: {execution_result.order_id})",
                    priority=AlertPriority.NORMAL
                )
            
            return execution_result
            
        except Exception as e:
            await self.alert_manager.send_alert(
                f"🚨 EXECUTION ERROR: {str(e)}",
                priority=AlertPriority.CRITICAL
            )
            raise
    
    async def _cancel_pending_orders(self, symbol: str):
        """
        Cancel all pending orders for symbol.
        
        CRITICAL: Prevents duplicate positions.
        Moon Dev learned this the hard way.
        """
        try:
            open_orders = await self.exchange.get_open_orders(symbol)
            
            for order in open_orders:
                await self.exchange.cancel_order(order.id)
                await asyncio.sleep(0.1)  # Rate limit protection
                
        except Exception as e:
            # Log but don't fail - exchange might have no open orders
            logger.warning(f"Error canceling orders for {symbol}: {e}")
    
    async def _has_position(self, symbol: str) -> bool:
        """
        Check if we already have a position in this symbol.
        """
        try:
            positions = await self.exchange.get_positions()
            return any(p.symbol == symbol and p.size > 0 for p in positions)
        except Exception as e:
            logger.error(f"Error checking position: {e}")
            # Fail safe - assume we have position if we can't check
            return True
    
    async def _normalize_order(self, order: Order) -> Order:
        """
        Normalize order to exchange requirements.
        
        CRITICAL: Wrong decimals = rejected orders
        """
        market_info = await self.exchange.get_market_info(order.symbol)
        
        # Round price to correct decimals
        price_precision = market_info.price_precision
        normalized_price = round(order.price, price_precision)
        
        # Round size to correct decimals
        size_precision = market_info.size_precision
        normalized_size = round(order.size, size_precision)
        
        # Round stop loss / take profit
        normalized_sl = round(order.stop_loss, price_precision) if order.stop_loss else None
        normalized_tp = round(order.take_profit, price_precision) if order.take_profit else None
        
        return Order(
            symbol=order.symbol,
            side=order.side,
            order_type=order.order_type,
            price=normalized_price,
            size=normalized_size,
            stop_loss=normalized_sl,
            take_profit=normalized_tp
        )
    
    async def _execute_with_retry(self, order: Order) -> ExecutionResult:
        """
        Execute order with exponential backoff retry.
        """
        return await self.retry_handler.execute(
            self.exchange.place_order,
            order
        )
```

#### 2. **Order Manager** (`execution/engine/order_manager.py`)
```python
# execution/engine/order_manager.py

class OrderManager:
    """
    Manage order lifecycle from placement to fill.
    
    Responsibilities:
    - Track order status
    - Monitor fills (partial/complete)
    - Handle rejections
    - Update positions
    """
    
    def __init__(
        self,
        exchange: BaseExchange,
        order_repo: OrderRepository,
        position_tracker: PositionTracker,
        event_bus: EventBus
    ):
        self.exchange = exchange
        self.order_repo = order_repo
        self.position_tracker = position_tracker
        self.event_bus = event_bus
        self.active_orders = {}  # order_id -> Order
        
    async def start(self):
        """
        Start monitoring orders via WebSocket.
        """
        await self.exchange.subscribe_user_data(
            on_order_update=self._handle_order_update
        )
    
    async def _handle_order_update(self, update: OrderUpdate):
        """
        Handle order update from exchange.
        
        Update types:
        - NEW: Order placed
        - PARTIALLY_FILLED: Partial fill
        - FILLED: Complete fill
        - CANCELED: Order canceled
        - REJECTED: Order rejected
        """
        order_id = update.order_id
        
        if update.status == OrderStatus.FILLED:
            await self._handle_fill(update)
        elif update.status == OrderStatus.PARTIALLY_FILLED:
            await self._handle_partial_fill(update)
        elif update.status == OrderStatus.REJECTED:
            await self._handle_rejection(update)
        elif update.status == OrderStatus.CANCELED:
            await self._handle_cancellation(update)
        
        # Update repository
        await self.order_repo.update_status(order_id, update.status)
        
        # Publish event
        await self.event_bus.publish(
            'orders:events',
            OrderUpdateEvent(
                order_id=order_id,
                status=update.status,
                filled_size=update.filled_size,
                timestamp=datetime.utcnow()
            )
        )
    
    async def _handle_fill(self, update: OrderUpdate):
        """
        Handle complete order fill.
        """
        # Update position tracker
        await self.position_tracker.update_position(
            symbol=update.symbol,
            side=update.side,
            size=update.filled_size,
            price=update.average_price
        )
        
        # Calculate P&L if closing
        if update.reduces_position:
            pnl = await self.position_tracker.calculate_pnl(update)
            
        # Remove from active orders
        self.active_orders.pop(update.order_id, None)
        
        logger.info(f"Order filled: {update.order_id} - {update.symbol}")
    
    async def _handle_partial_fill(self, update: OrderUpdate):
        """
        Handle partial order fill.
        """
        logger.info(
            f"Partial fill: {update.order_id} - "
            f"{update.filled_size}/{update.total_size}"
        )
        
        # Update position with partial
        await self.position_tracker.update_position(
            symbol=update.symbol,
            side=update.side,
            size=update.filled_size,
            price=update.average_price,
            partial=True
        )
    
    async def _handle_rejection(self, update: OrderUpdate):
        """
        Handle order rejection.
        """
        logger.error(f"Order rejected: {update.order_id} - {update.reject_reason}")
        
        # Alert critical
        await self.alert_manager.send_alert(
            f"🚨 Order REJECTED: {update.symbol}\nReason: {update.reject_reason}",
            priority=AlertPriority.CRITICAL
        )
        
        # Remove from active
        self.active_orders.pop(update.order_id, None)
    
    async def _handle_cancellation(self, update: OrderUpdate):
        """
        Handle order cancellation.
        """
        logger.info(f"Order canceled: {update.order_id}")
        self.active_orders.pop(update.order_id, None)
```

#### 3. **Retry Logic** (`execution/retry/`)

**a) Exponential Backoff** (`execution/retry/exponential_backoff.py`)
```python
# execution/retry/exponential_backoff.py
import asyncio
from typing import Callable, TypeVar, Any
import random

T = TypeVar('T')

class ExponentialBackoff:
    """
    Exponential backoff with jitter for retries.
    
    Pattern:
    - Attempt 1: immediate
    - Attempt 2: wait 1s + jitter
    - Attempt 3: wait 2s + jitter
    - Attempt 4: wait 4s + jitter
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 10.0,
        jitter: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
    
    async def execute(
        self,
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> T:
        """
        Execute function with exponential backoff retry.
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                result = await func(*args, **kwargs)
                return result
                
            except Exception as e:
                last_exception = e
                
                if attempt == self.max_retries - 1:
                    # Last attempt failed
                    break
                
                # Calculate delay
                delay = min(
                    self.base_delay * (2 ** attempt),
                    self.max_delay
                )
                
                # Add jitter
                if self.jitter:
                    delay = delay * (0.5 + random.random())
                
                logger.warning(
                    f"Attempt {attempt + 1}/{self.max_retries} failed: {e}. "
                    f"Retrying in {delay:.2f}s..."
                )
                
                await asyncio.sleep(delay)
        
        # All retries failed
        raise Exception(
            f"All {self.max_retries} attempts failed. "
            f"Last error: {last_exception}"
        )
```

**b) Circuit Breaker** (`execution/retry/circuit_breaker.py`)
```python
# execution/retry/circuit_breaker.py
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing if recovered

class CircuitBreaker:
    """
    Circuit breaker pattern for execution.
    
    States:
    - CLOSED: Normal operation
    - OPEN: Too many failures, stop trying
    - HALF_OPEN: Test if service recovered
    
    Use case: Exchange API down, stop hammering it.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,  # seconds
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None
    
    async def call(self, func, *args, **kwargs):
        """
        Execute function through circuit breaker.
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker CLOSED (recovered)")
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.utcnow()
            logger.error(
                f"Circuit breaker OPENED after {self.failure_count} failures"
            )
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time passed to attempt reset."""
        if self.opened_at is None:
            return False
        
        return datetime.utcnow() - self.opened_at > timedelta(seconds=self.timeout)
```

#### 4. **Position Tracker** (`execution/engine/position_tracker.py`)
```python
# execution/engine/position_tracker.py

class PositionTracker:
    """
    Track open positions in real-time.
    
    Responsibilities:
    - Maintain position state
    - Calculate unrealized P&L
    - Calculate realized P&L on close
    - Sync with exchange periodically
    """
    
    def __init__(
        self,
        exchange: BaseExchange,
        position_repo: PositionRepository
    ):
        self.exchange = exchange
        self.position_repo = position_repo
        self.positions = {}  # symbol -> Position
        
    async def start(self):
        """
        Start position tracking.
        """
        # Load existing positions
        await self._sync_with_exchange()
        
        # Subscribe to price updates
        await self._subscribe_price_updates()
        
        # Periodic sync every 5 minutes
        asyncio.create_task(self._periodic_sync())
    
    async def update_position(
        self,
        symbol: str,
        side: OrderSide,
        size: Decimal,
        price: Decimal,
        partial: bool = False
    ):
        """
        Update position on order fill.
        """
        if symbol not in self.positions:
            # New position
            self.positions[symbol] = Position(
                symbol=symbol,
                side=side,
                size=size,
                entry_price=price,
                current_price=price,
                opened_at=datetime.utcnow()
            )
        else:
            # Existing position - average in or close
            position = self.positions[symbol]
            
            if side == position.side:
                # Adding to position - average price
                total_cost = (position.size * position.entry_price) + (size * price)
                total_size = position.size + size
                position.entry_price = total_cost / total_size
                position.size = total_size
            else:
                # Closing position (or reducing)
                if size >= position.size:
                    # Complete close
                    realized_pnl = self._calculate_realized_pnl(position, price, position.size)
                    await self._close_position(symbol, realized_pnl)
                else:
                    # Partial close
                    realized_pnl = self._calculate_realized_pnl(position, price, size)
                    position.size -= size
                    position.realized_pnl += realized_pnl
        
        # Save to repository
        await self.position_repo.save(self.positions[symbol])
    
    async def _close_position(self, symbol: str, realized_pnl: Decimal):
        """
        Close position completely.
        """
        position = self.positions.pop(symbol)
        position.status = PositionStatus.CLOSED
        position.closed_at = datetime.utcnow()
        position.realized_pnl = realized_pnl
        
        await self.position_repo.save(position)
        
        logger.info(
            f"Position closed: {symbol} - "
            f"P&L: ${realized_pnl:.2f}"
        )
    
    def _calculate_realized_pnl(
        self,
        position: Position,
        exit_price: Decimal,
        size: Decimal
    ) -> Decimal:
        """
        Calculate realized P&L.
        """
        if position.side == OrderSide.BUY:
            pnl = (exit_price - position.entry_price) * size
        else:
            pnl = (position.entry_price - exit_price) * size
        
        return pnl
    
    def calculate_unrealized_pnl(self, symbol: str) -> Decimal:
        """
        Calculate unrealized P&L for open position.
        """
        if symbol not in self.positions:
            return Decimal(0)
        
        position = self.positions[symbol]
        
        if position.side == OrderSide.BUY:
            pnl = (position.current_price - position.entry_price) * position.size
        else:
            pnl = (position.entry_price - position.current_price) * position.size
        
        return pnl
    
    async def _sync_with_exchange(self):
        """
        Sync positions with exchange.
        
        CRITICAL: Ensures we have correct state.
        """
        try:
            exchange_positions = await self.exchange.get_positions()
            
            for ex_pos in exchange_positions:
                if ex_pos.size > 0:
                    self.positions[ex_pos.symbol] = Position(
                        symbol=ex_pos.symbol,
                        side=ex_pos.side,
                        size=ex_pos.size,
                        entry_price=ex_pos.entry_price,
                        current_price=ex_pos.mark_price,
                        opened_at=ex_pos.opened_at
                    )
            
            logger.info(f"Synced {len(self.positions)} positions with exchange")
            
        except Exception as e:
            logger.error(f"Error syncing positions: {e}")
    
    async def _periodic_sync(self):
        """
        Periodically sync with exchange (every 5 min).
        """
        while True:
            await asyncio.sleep(300)  # 5 minutes
            await self._sync_with_exchange()
```

### **Criterios de Aceptación**:
- ✅ Orders ejecutadas correctamente en testnet
- ✅ Retry logic funciona (test con API down)
- ✅ Position tracking es accurado (±$0.01)
- ✅ Duplicate orders prevenidas (100% de los casos)
- ✅ Circuit breaker funciona
- ✅ <50ms p99 execution time (measure con prometheus)
- ✅ All errors logged con contexto completo

### **Entregables**:
- OrderExecutor implementado y testeado
- OrderManager con WebSocket integration
- Retry logic (exponential backoff + circuit breaker)
- PositionTracker con sync automático
- 20+ integration tests (testnet)
- Performance benchmarks documentados

---

## **Sprint 7.2: Order Types & Advanced Execution**
**Duración**: 2 días

### Tareas:

#### 1. **Order Type Handlers** (`execution/order_types/`)

**a) Market Orders** (`execution/order_types/market.py`)
```python
# execution/order_types/market.py

class MarketOrderHandler:
    """
    Handle market order execution.
    
    Market orders:
    - Execute immediately at best available price
    - Higher slippage risk
    - Guaranteed fill (usually)
    """
    
    async def execute(self, order: Order) -> ExecutionResult:
        """
        Execute market order.
        """
        # Validate it's a market order
        if order.order_type != OrderType.MARKET:
            raise ValueError("Not a market order")
        
        # Market orders don't have price - use None
        order.price = None
        
        # Execute
        result = await self.exchange.place_market_order(
            symbol=order.symbol,
            side=order.side,
            size=order.size
        )
        
        return ExecutionResult(
            success=True,
            order_id=result.order_id,
            filled_price=result.filled_price,
            filled_size=result.filled_size
        )
```

**b) Limit Orders** (`execution/order_types/limit.py`)
```python
# execution/order_types/limit.py

class LimitOrderHandler:
    """
    Handle limit order execution.
    
    Limit orders:
    - Execute at specified price or better
    - May not fill immediately
    - Better price control
    """
    
    async def execute(self, order: Order) -> ExecutionResult:
        """
        Execute limit order.
        """
        if order.order_type != OrderType.LIMIT:
            raise ValueError("Not a limit order")
        
        # Validate price is set
        if order.price is None:
            raise ValueError("Limit order requires price")
        
        # Place limit order
        result = await self.exchange.place_limit_order(
            symbol=order.symbol,
            side=order.side,
            size=order.size,
            price=order.price
        )
        
        return ExecutionResult(
            success=True,
            order_id=result.order_id,
            status=OrderStatus.PENDING
        )
```

**c) Stop Loss Orders** (`execution/order_types/stop_loss.py`)
```python
# execution/order_types/stop_loss.py

class StopLossHandler:
    """
    Handle stop loss orders.
    
    CRITICAL: Stop losses protect from large losses.
    """
    
    async def execute(self, order: Order) -> ExecutionResult:
        """
        Place stop loss order.
        """
        if order.stop_loss is None:
            raise ValueError("Stop loss price required")
        
        # For Binance: use STOP_MARKET
        result = await self.exchange.place_stop_order(
            symbol=order.symbol,
            side=OrderSide.SELL if order.side == OrderSide.BUY else OrderSide.BUY,
            size=order.size,
            stop_price=order.stop_loss,
            order_type='STOP_MARKET'
        )
        
        return ExecutionResult(
            success=True,
            order_id=result.order_id,
            status=OrderStatus.PENDING
        )
```

**d) OCO Orders** (`execution/order_types/oco.py`)
```python
# execution/order_types/oco.py

class OCOHandler:
    """
    One-Cancels-Other orders.
    
    Place both take profit and stop loss.
    When one fills, cancel the other.
    """
    
    async def execute(self, order: Order) -> ExecutionResult:
        """
        Place OCO order (TP + SL).
        """
        if not order.take_profit or not order.stop_loss:
            raise ValueError("OCO requires both TP and SL")
        
        # Binance OCO
        result = await self.exchange.place_oco_order(
            symbol=order.symbol,
            side=order.side,
            size=order.size,
            price=order.price,  # Limit price
            stop_price=order.stop_loss,
            stop_limit_price=order.stop_loss * Decimal('0.99'),  # Stop limit
            take_profit_price=order.take_profit
        )
        
        return ExecutionResult(
            success=True,
            order_id=result.order_id,
            oco_id=result.oco_id
        )
```

#### 2. **Smart Order Router** (`execution/engine/router.py`)
```python
# execution/engine/router.py

class SmartOrderRouter:
    """
    Route orders to best execution venue.
    
    Considerations:
    - Liquidity
    - Fees (maker/taker)
    - Latency
    - Available balance
    """
    
    def __init__(self, exchanges: List[BaseExchange]):
        self.exchanges = exchanges
    
    async def route(self, order: Order) -> BaseExchange:
        """
        Select best exchange for order.
        
        Criteria:
        1. Has the symbol
        2. Has liquidity
        3. Lowest fees
        4. Lowest latency (if HFT)
        """
        candidates = []
        
        for exchange in self.exchanges:
            # Check if exchange supports symbol
            if not await exchange.has_market(order.symbol):
                continue
            
            # Get orderbook depth
            depth = await exchange.get_orderbook_depth(order.symbol)
            
            # Get fees
            fees = await exchange.get_fees(order.symbol)
            
            # Calculate effective cost
            effective_cost = self._calculate_cost(order, depth, fees)
            
            candidates.append({
                'exchange': exchange,
                'cost': effective_cost,
                'depth': depth
            })
        
        if not candidates:
            raise Exception(f"No exchange supports {order.symbol}")
        
        # Select lowest cost
        best = min(candidates, key=lambda x: x['cost'])
        
        return best['exchange']
    
    def _calculate_cost(self, order, depth, fees):
        """
        Calculate total execution cost.
        
        Includes:
        - Trading fees
        - Estimated slippage
        """
        # Fee cost
        fee_cost = order.size * order.price * fees.taker_fee
        
        # Slippage (estimate from orderbook)
        slippage = self._estimate_slippage(order, depth)
        
        return fee_cost + slippage
```

### **Criterios de Aceptación**:
- ✅ All order types implementados
- ✅ OCO orders funcionan correctamente
- ✅ Smart router selecciona exchange óptimo
- ✅ Stop loss se ejecuta automáticamente
- ✅ 15+ tests para cada order type

### **Entregables**:
- Order type handlers completos
- Smart order router
- 20+ tests
- Documentation de cada order type

---

## **Sprint 7.3: Execution Simulation & Testing**
**Duración**: 2 días

### Tareas:

#### 1. **Fill Simulator** (`execution/simulation/fill_simulator.py`)
```python
# execution/simulation/fill_simulator.py

class FillSimulator:
    """
    Simulate order fills for backtesting.
    
    Simulates:
    - Partial fills
    - Slippage
    - Market impact
    - Reject scenarios
    """
    
    def __init__(
        self,
        slippage_model: SlippageModel,
        market_impact_model: MarketImpactModel
    ):
        self.slippage_model = slippage_model
        self.market_impact_model = market_impact_model
    
    def simulate_fill(
        self,
        order: Order,
        orderbook: OrderBook,
        market_conditions: MarketConditions
    ) -> FillResult:
        """
        Simulate order fill.
        
        Returns:
            FillResult with filled price/size
        """
        if order.order_type == OrderType.MARKET:
            return self._simulate_market_fill(order, orderbook)
        elif order.order_type == OrderType.LIMIT:
            return self._simulate_limit_fill(order, orderbook)
    
    def _simulate_market_fill(self, order, orderbook) -> FillResult:
        """
        Simulate market order fill.
        """
        # Market orders walk the orderbook
        if order.side == OrderSide.BUY:
            available_liquidity = orderbook.asks
        else:
            available_liquidity = orderbook.bids
        
        filled_size = Decimal(0)
        total_cost = Decimal(0)
        
        for level in available_liquidity:
            level_price = level.price
            level_size = level.size
            
            remaining = order.size - filled_size
            fill_at_level = min(remaining, level_size)
            
            filled_size += fill_at_level
            total_cost += fill_at_level * level_price
            
            if filled_size >= order.size:
                break
        
        if filled_size < order.size:
            # Partial fill only
            pass
        
        average_price = total_cost / filled_size if filled_size > 0 else Decimal(0)
        
        # Add slippage
        slippage = self.slippage_model.calculate(order, market_conditions)
        final_price = average_price * (Decimal(1) + slippage)
        
        return FillResult(
            filled_size=filled_size,
            filled_price=final_price,
            is_partial=filled_size < order.size
        )
```

#### 2. **Execution Tests** (`tests/integration/test_execution_flow.py`)
```python
# tests/integration/test_execution_flow.py
import pytest
import asyncio

@pytest.mark.asyncio
class TestExecutionFlow:
    """
    Integration tests for execution flow.
    """
    
    async def test_full_order_flow(self, executor, test_order):
        """
        Test complete order flow: place → fill → position update.
        """
        # Place order
        result = await executor.execute(test_order)
        
        assert result.success
        assert result.order_id is not None
        
        # Wait for fill (simulate)
        await asyncio.sleep(2)
        
        # Check# ROADMAP - Fases Faltantes (8, 9, 10)

## Contenido a agregar al final del ROADMAP.md

### **Criterios de Aceptación**:
- ✅ Fill simulator realista
- ✅ Slippage model validado
- ✅ Integration tests completos
- ✅ Testnet execution funciona
- ✅ 25+ tests pasando

### **Entregables**:
- Fill simulator completo
- Execution test suite
- Testnet validation report
- Performance benchmarks

---

## 📊 FASE 8: MONITORING & ALERTS (Semana 10)

### **Sprint 8.1: Metrics Collection & Prometheus**
**Duración**: 2-3 días

#### Tareas:

1. **Prometheus Integration** (`monitoring/prometheus/`)
   - [ ] `metrics_collector.py`: Collect system metrics
     - Order execution latency (histogram)
     - Order success/failure rate (counter)
     - Position count (gauge)
     - Portfolio value (gauge)
     - API latency per exchange (histogram)
     - WebSocket connection status (gauge)
   
   - [ ] `prometheus_exporter.py`: Expose metrics endpoint
   - [ ] `prometheus.yml`: Prometheus config

2. **Custom Metrics** (`monitoring/metrics/`)
   - [ ] `trading_metrics.py`:
     - Daily PnL
     - Win rate (24h rolling)
     - Sharpe ratio (real-time estimate)
     - Max drawdown (current)
     - Active positions
     - Capital utilization
   
   - [ ] `system_metrics.py`:
     - Memory usage
     - CPU usage
     - Disk I/O
     - Network I/O
     - Redis/DB connection pool status

3. **Health Checks** (`monitoring/health/`)
   - [ ] `health_checker.py`: System health endpoint
   - [ ] Check database connectivity
   - [ ] Check Redis connectivity
   - [ ] Check exchange API
   - [ ] Check WebSocket connections
   - [ ] Check disk space

**Criterios de Aceptación**:
- ✅ Prometheus scraping funciona
- ✅ All metrics exportados correctamente
- ✅ Health endpoint responde <100ms
- ✅ Metrics retention 30+ días
- ✅ Grafana puede query metrics

**Entregables**:
- Prometheus setup completo
- 20+ custom metrics
- Health check endpoint
- Metrics documentation

---

### **Sprint 8.2: Grafana Dashboards**
**Duración**: 2 días

#### Tareas:

1. **System Health Dashboard** (`monitoring/grafana/dashboards/system_health.json`)
   - [ ] Uptime panel
   - [ ] API latency (p50, p95, p99)
   - [ ] Memory/CPU usage
   - [ ] Connection status (DB, Redis, Exchange)
   - [ ] Error rate
   - [ ] Request rate

2. **Trading Performance Dashboard** (`monitoring/grafana/dashboards/trading.json`)
   - [ ] Real-time PnL (gauge + time series)
   - [ ] Daily/Weekly/Monthly returns
   - [ ] Win rate (24h rolling)
   - [ ] Active positions table
   - [ ] Recent trades table
   - [ ] Portfolio allocation pie chart

3. **Risk Dashboard** (`monitoring/grafana/dashboards/risk.json`)
   - [ ] Current drawdown vs max
   - [ ] VaR utilization
   - [ ] Leverage usage
   - [ ] Position concentration
   - [ ] Circuit breaker status
   - [ ] Risk limit alerts

4. **Strategy Dashboard** (`monitoring/grafana/dashboards/strategy.json`)
   - [ ] Signals generated (per strategy)
   - [ ] Signal conversion rate
   - [ ] Strategy PnL breakdown
   - [ ] Strategy win rate
   - [ ] Average hold time

**Criterios de Aceptación**:
- ✅ 4 dashboards funcionando
- ✅ Real-time updates (<15s delay)
- ✅ Mobile-friendly
- ✅ Exportable/importable
- ✅ Alerting configurado

**Entregables**:
- 4 Grafana dashboards
- Dashboard screenshots
- Setup documentation

---

### **Sprint 8.3: Alert System**
**Duración**: 2 días

#### Tareas:

1. **Alert Manager** (`alerting/alert_manager.py`)
   - [ ] Implement alert manager with rate limiting
   - [ ] Support multiple channels
   - [ ] Priority-based routing
   - [ ] Alert history tracking
   - [ ] Deduplication logic

2. **Alert Channels** (`alerting/channels/`)
   - [ ] **Telegram** (`telegram.py`): Send messages to Telegram bot
   - [ ] **Discord** (`discord.py`): Send to Discord webhook
   - [ ] **Email** (`email.py`): SMTP integration
   - [ ] **SMS** (`sms.py`): Twilio integration (opcional)

3. **Alert Rules** (`alerting/rules/`)
   - [ ] `trading_alerts.py`:
     - Order filled
     - Order rejected
     - Position opened/closed
     - Daily loss limit approaching
     - Circuit breaker triggered
   
   - [ ] `system_alerts.py`:
     - API connection lost
     - Database connection lost
     - High latency detected
     - Disk space low
     - Memory usage high

**Criterios de Aceptación**:
- ✅ Alerts llegan en <5s
- ✅ Rate limiting funciona
- ✅ All channels funcionan
- ✅ Priority routing correcto
- ✅ No duplicate alerts

**Entregables**:
- Alert system completo
- 4 alert channels
- 10+ alert rules
- Alert testing suite

---

## 🔒 FASE 9: PRODUCTION HARDENING (Semana 11)

### **Sprint 9.1: Security & Secrets Management**
**Duración**: 2 días

#### Tareas:

1. **Secrets Management**
   - [ ] Migrate from .env to secure vault
   - [ ] Use AWS Secrets Manager o HashiCorp Vault
   - [ ] Rotate API keys programmatically
   - [ ] Encrypt sensitive data at rest

2. **API Security**
   - [ ] Add API key authentication
   - [ ] Rate limiting per API key
   - [ ] CORS configuration
   - [ ] Input validation y sanitization

3. **Audit Logging** (`infrastructure/logging/audit_logger.py`)
   - [ ] Log all order placements
   - [ ] Log all configuration changes
   - [ ] Log all API access
   - [ ] Tamper-proof logs (append-only)

**Criterios de Aceptación**:
- ✅ No secrets en código
- ✅ API keys rotables
- ✅ Audit trail completo
- ✅ Security scan passed

---

### **Sprint 9.2: Error Handling & Recovery**
**Duración**: 2 días

#### Tareas:

1. **Graceful Degradation**
   - [ ] Fallback to cached data si DB down
   - [ ] Queue orders si exchange API down
   - [ ] Continue con partial data
   - [ ] Auto-recovery procedures

2. **Dead Letter Queues**
   - [ ] DLQ para failed events
   - [ ] DLQ para failed orders
   - [ ] Retry mechanism con backoff
   - [ ] Manual review interface

3. **Crash Recovery** (`infrastructure/recovery/`)
   - [ ] State persistence
   - [ ] Resume from last checkpoint
   - [ ] Reconcile positions con exchange
   - [ ] Detect and fix inconsistencies

**Criterios de Aceptación**:
- ✅ System recovers automáticamente
- ✅ No data loss en crashes
- ✅ Positions reconciled correctamente
- ✅ DLQ procesado correctamente

---

### **Sprint 9.3: Performance Optimization**
**Duración**: 3 días

#### Tareas:

1. **Database Optimization**
   - [ ] Add indexes para queries frecuentes
   - [ ] Optimize query plans
   - [ ] Connection pool tuning
   - [ ] Enable TimescaleDB compression

2. **Caching Strategy**
   - [ ] Cache candles (TTL 1min)
   - [ ] Cache orderbook snapshots
   - [ ] Cache market info
   - [ ] Implement cache warming

3. **Code Profiling**
   - [ ] Profile con cProfile
   - [ ] Identify bottlenecks
   - [ ] Optimize hot paths
   - [ ] Reduce memory allocations

4. **Load Testing** (`tests/performance/`)
   - [ ] Test con 10k orders/min
   - [ ] Test con 100 concurrent strategies
   - [ ] Test con 50 symbols
   - [ ] Measure p99 latency

**Criterios de Aceptación**:
- ✅ Order execution <50ms p99
- ✅ Backtest 1 year <5min
- ✅ Memory usage <2GB
- ✅ Can handle 10k orders/min
- ✅ Database queries <10ms p95

---

### **Sprint 9.4: Deployment & CI/CD**
**Duración**: 2 días

#### Tareas:

1. **Docker Production Images**
   - [ ] Multi-stage builds
   - [ ] Minimize image size
   - [ ] Security scanning
   - [ ] Version tagging

2. **CI/CD Pipeline** (`.github/workflows/`)
   - [ ] Automated testing on push
   - [ ] Linting and type checking
   - [ ] Docker image building
   - [ ] Automated deployment

3. **Deployment Scripts** (`scripts/`)
   - [ ] `deploy.sh`: Deploy to production
   - [ ] `rollback.sh`: Rollback deployment
   - [ ] `backup.sh`: Backup database
   - [ ] `restore.sh`: Restore from backup

**Criterios de Aceptación**:
- ✅ CI/CD pipeline funciona
- ✅ Automated testing
- ✅ Zero-downtime deployment
- ✅ Rollback capability
- ✅ Automated backups

---

## 🚀 FASE 10: ADVANCED FEATURES (Ongoing)

### **Sprint 10.1: Regime Detection**
**Duración**: 1 semana

#### Tareas:

1. **Feature Engineering** (`regime_detection/features/`)
   - [ ] Volatility features (ATR, Bollinger width)
   - [ ] Trend features (ADX, slope)
   - [ ] Volume features (OBV, volume profile)
   - [ ] Correlation features

2. **Regime Classifier** (`regime_detection/regime_classifier.py`)
   - [ ] K-means clustering
   - [ ] Hidden Markov Model
   - [ ] Label regimes: Trending, Ranging, Volatile, Calm

3. **Strategy Mapper** (`regime_detection/strategy_mapper.py`)
   - [ ] Map regimes to optimal strategies
   - [ ] Auto-switch strategies based on regime
   - [ ] Backtest per regime

**Entregables**:
- Regime detection system
- Strategy-regime mapping
- Regime-specific backtests

---

### **Sprint 10.2: Machine Learning Integration**
**Duración**: 2 semanas

#### Tareas:

1. **ML Pipeline** (`strategies/ml/`)
   - [ ] Feature engineering
   - [ ] Model training pipeline
   - [ ] Model versioning (MLflow)
   - [ ] A/B testing framework

2. **Models**
   - [ ] LSTM for price prediction
   - [ ] Random Forest for signal classification
   - [ ] XGBoost for feature importance
   - [ ] Ensemble methods

3. **Online Learning**
   - [ ] Incremental model updates
   - [ ] Drift detection
   - [ ] Auto-retraining triggers

**Entregables**:
- ML pipeline completo
- 3+ trained models
- Model monitoring dashboard

---

### **Sprint 10.3: Portfolio Optimization**
**Duración**: 1 semana

#### Tareas:

1. **Modern Portfolio Theory** (`portfolio/optimization/`)
   - [ ] Mean-variance optimization
   - [ ] Sharpe ratio maximization
   - [ ] Risk parity
   - [ ] Black-Litterman model

2. **Dynamic Allocation**
   - [ ] Rebalance based on performance
   - [ ] Adjust based on market conditions
   - [ ] Kelly criterion for position sizing

**Entregables**:
- Portfolio optimizer
- Rebalancing engine
- Allocation backtests

---

### **Sprint 10.4: Multi-Exchange Arbitrage**
**Duración**: 1 semana

#### Tareas:

1. **Arbitrage Scanner** (`strategies/arbitrage/`)
   - [ ] Cross-exchange price monitoring
   - [ ] Triangular arbitrage detection
   - [ ] Funding rate arbitrage

2. **Execution**
   - [ ] Simultaneous execution
   - [ ] Transfer time consideration
   - [ ] Fee optimization

**Entregables**:
- Arbitrage scanner
- Multi-exchange executor
- Arbitrage backtests

---

## 📝 RESUMEN FINAL

### Timeline Completo:

| Fase | Duración | Entregables Clave |
|------|----------|-------------------|
| **Fase 0** | 3-5 días | Setup completo, Domain layer |
| **Fase 1** | 1-2 semanas | Database, Exchange connectors, Message bus |
| **Fase 2** | 1 semana | Market data pipeline, Historical data |
| **Fase 3** | 1 semana | Strategy framework, Breakout strategy |
| **Fase 4** | 1-2 semanas | Backtesting engine, Optimization |
| **Fase 5** | 1 semana | Scanner system |
| **Fase 6** | 1 semana | Risk management completo |
| **Fase 7** | 1 semana | Execution engine |
| **Fase 8** | 3-5 días | Monitoring, Alerts |
| **Fase 9** | 1 semana | Production hardening |
| **Fase 10** | Ongoing | Advanced features |

**Total MVP**: 8-10 semanas
**Total Production-Ready**: 12-14 semanas
**Total con Advanced Features**: 16-20 semanas

### Métricas de Éxito:

- ✅ **Performance**: <50ms p99 execution latency
- ✅ **Reliability**: 99.9%+ uptime
- ✅ **Throughput**: 10,000+ orders/min
- ✅ **Testing**: 200+ tests, >80% coverage
- ✅ **Documentation**: Complete API docs, architecture docs
- ✅ **Security**: No secrets in code, audit logging
- ✅ **Monitoring**: Real-time dashboards, alerting

### Próximos Pasos:

1. **Empezar con Fase 0**: Setup environment
2. **Seguir el roadmap secuencialmente**: No saltar fases
3. **Validar cada sprint**: Criterios de aceptación deben cumplirse
4. **Iterar y mejorar**: Feedback loop continuo
5. **Documentar todo**: Mantener docs actualizados

---

**¡IMPORTANTE!**: Este roadmap es una guía. Ajusta según necesidades, pero mantén la filosofía RBI: **Research → Backtest → Implement**. Nunca saltes directo a producción sin validación exhaustiva.
